# SevaSarathi ROS 2 Test Bridge

This package is only for proving the Phase 1 web application can reach ROS 2.

Flow:

Web App -> Express -> HTTP POST :9000/delivery-request -> ROS 2 -> /sevasarathi/delivery_request

## Build

```bash
cd ~/ros2_ws/src
# copy the sevasarathi_ros_test package here
cd ~/ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --packages-select sevasarathi_ros_test
source install/setup.bash
```

## Start bridge

```bash
ros2 run sevasarathi_ros_test ros_test_bridge
```

Keep the bridge terminal running while using the web application. The bridge
listens on `0.0.0.0:9000`, which allows the Express Docker container to reach
it through `http://host.docker.internal:9000`.

Verify the bridge before submitting a request:

```bash
curl http://localhost:9000/health
```

Expected response:

```json
{"status":"ok","ros_topic":"/sevasarathi/delivery_request"}
```

If ROS 2 runs inside WSL, its networking must expose port 9000 to Windows.
Otherwise run the bridge where Windows and Docker Desktop can reach it.

## Start listener in another terminal

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run sevasarathi_ros_test ros_test_listener
```

## Check HTTP health

```bash
curl http://localhost:9000/health
```

## Check ROS topic

```bash
ros2 topic list | grep sevasarathi
ros2 topic echo /sevasarathi/delivery_request
```

## Manual HTTP test

```bash
curl -X POST http://localhost:9000/delivery-request \
  -H 'Content-Type: application/json' \
  -d '{"request_id":"test-001","pickup_location":"PHARMACY","dropoff_location":"ICU","priority":"NORMAL","item":"Blood Samples","requested_by":"manual-test","created_at":"2026-08-24T00:00:00Z"}'
```
