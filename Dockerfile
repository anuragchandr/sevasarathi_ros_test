FROM ros:humble

SHELL ["/bin/bash", "-c"]

WORKDIR /ros_ws

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

COPY ./sevasarathi_ros_test /ros_ws/src/sevasarathi_ros_test

RUN rosdep init || true && \
    rosdep update && \
    cd /ros_ws && \
    rosdep install --from-paths src --ignore-src -r -y --rosdistro humble && \
    . /opt/ros/humble/setup.bash && \
    colcon build --packages-select sevasarathi_ros_test --cmake-args -DCMAKE_BUILD_TYPE=Release

CMD ["bash", "-lc", "source /opt/ros/humble/setup.bash && source /ros_ws/install/setup.bash && ros2 run sevasarathi_ros_test ros_test_bridge"]
