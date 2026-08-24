#!/usr/bin/env python3
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

TOPIC = '/sevasarathi/delivery_request'
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 9000


class RosTestBridge(Node):
    def __init__(self):
        super().__init__('sevasarathi_ros_test_bridge')
        self.publisher = self.create_publisher(String, TOPIC, 10)
        self.get_logger().info(f'ROS publisher ready: {TOPIC}')

    def publish_request(self, request_data):
        message = String()
        message.data = json.dumps(request_data, separators=(',', ':'))
        self.publisher.publish(message)
        self.get_logger().info(
            f"Published request {request_data.get('request_id')} "
            f"{request_data.get('pickup_location')} -> {request_data.get('dropoff_location')}"
        )


bridge_node = None


class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        response = json.dumps(payload).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == '/health':
            self._send_json(200, {'status': 'ok', 'ros_topic': TOPIC})
            return
        self._send_json(404, {'message': 'Not found'})

    def do_POST(self):
        if self.path != '/delivery-request':
            self._send_json(404, {'message': 'Not found'})
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            raw_body = self.rfile.read(content_length)
            request_data = json.loads(raw_body.decode('utf-8'))

            required = ['request_id', 'pickup_location', 'dropoff_location']
            missing = [field for field in required if not request_data.get(field)]
            if missing:
                self._send_json(400, {'message': f'Missing fields: {", ".join(missing)}'})
                return

            bridge_node.publish_request(request_data)

            self._send_json(202, {
                'status': 'accepted',
                'message': 'Delivery request published to ROS 2',
                'request_id': request_data['request_id'],
                'topic': TOPIC,
            })
        except json.JSONDecodeError:
            self._send_json(400, {'message': 'Request body must be valid JSON'})
        except Exception as error:
            print(f'[HTTP] Error: {error}')
            self._send_json(500, {'message': 'ROS bridge error'})

    def log_message(self, format, *args):
        print(f'[HTTP] {self.address_string()} - {format % args}')


def main(args=None):
    global bridge_node

    rclpy.init(args=args)
    bridge_node = RosTestBridge()

    http_server = ThreadingHTTPServer((HTTP_HOST, HTTP_PORT), RequestHandler)
    http_thread = threading.Thread(target=http_server.serve_forever, daemon=True)
    http_thread.start()

    bridge_node.get_logger().info(f'HTTP bridge listening on http://{HTTP_HOST}:{HTTP_PORT}')
    bridge_node.get_logger().info('POST /delivery-request -> ROS 2 topic')

    try:
        rclpy.spin(bridge_node)
    except KeyboardInterrupt:
        pass
    finally:
        http_server.shutdown()
        http_server.server_close()
        bridge_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
