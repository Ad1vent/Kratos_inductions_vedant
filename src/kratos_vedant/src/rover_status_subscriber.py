#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import std_msgs
from std_msgs import msg
from std_msgs.msg import Float32, String, Bool

class rover_status_subscriber(Node):

    def __init__(self):

        super().__init__("rover_status_subscriber")
        self.get_logger().info("rover_status_subscriber node has started")

        self.battery_subscriber = self.create_subscription(Float32, "/rover/battery_status", self.battery_callback, 10)
        self.mode_subscriber = self.create_subscription(String, "/rover/mode", self.mode_callback, 10)
        self.stop_subscriber = self.create_subscription(Bool, "/rover/stop", self.stop_callback, 10)

    def battery_callback(self, msg: Float32):
        self.get_logger().info(f"Battery Level: {msg.data:.1f}")

    def mode_callback(self, msg: String):
        self.get_logger().info(f"Mode: {msg.data}")
        
    def stop_callback(self, msg: Bool):

        if msg.data==True:
            self.get_logger().info("Emergency Stop Activated (or) Rover is out of battery.")
        else:
            self.get_logger().info("Rover is ON.")


def main(args=None):

    rclpy.init(args=args)

    node=rover_status_subscriber()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()