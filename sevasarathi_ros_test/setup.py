from setuptools import setup

package_name = 'sevasarathi_ros_test'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'ros_test_bridge = sevasarathi_ros_test.ros_test_bridge:main',
            'ros_test_listener = sevasarathi_ros_test.ros_test_listener:main',
        ],
    },
)
