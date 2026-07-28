#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from kratos_vedant_msgs.msg import RoverStatus

class rover_status_subscriber(Node):

    def __init__(self):

        super().__init__("rover_status_subscriber")
        self.get_logger().info("rover_status_subscriber node has started")

        self.status_subscriber = self.create_subscription(RoverStatus, "/rover/status", self.status_callback, 10)


    def status_callback(self, msg: RoverStatus):

        self.get_logger().info(f"Battery Level: {msg.battery_percentage:.1f}")
        self.get_logger().info(f"Mode: {msg.mode}")

        if msg.emergency_stop==True:
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