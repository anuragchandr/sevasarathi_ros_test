#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

TOPIC = '/sevasarathi/delivery_request'


class RosTestListener(Node):
    def __init__(self):
        super().__init__('sevasarathi_ros_test_listener')
        self.subscription = self.create_subscription(
            String,
            TOPIC,
            self.request_callback,
            10,
        )
        self.get_logger().info(f'Listening on {TOPIC}')

    def request_callback(self, message):
        try:
            request = json.loads(message.data)
            print('\n========== SEVASARATHI DELIVERY REQUEST ==========')
            print(f"Request ID : {request.get('request_id')}")
            print(f"Pickup     : {request.get('pickup_location')}")
            print(f"Destination: {request.get('dropoff_location')}")
            print(f"Priority   : {request.get('priority')}")
            print(f"Item       : {request.get('item')}")
            print(f"Requested by: {request.get('requested_by')}")
            print(f"Created at : {request.get('created_at')}")
            print('==================================================\n')
        except json.JSONDecodeError:
            self.get_logger().error(f'Invalid JSON received: {message.data}')


def main(args=None):
    rclpy.init(args=args)
    node = RosTestListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
