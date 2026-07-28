#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import std_msgs
from std_msgs.msg import Float32, String, Bool


class rover_status_publisher(Node):

    def __init__(self):

        super().__init__("rover_status_publisher")
        self.get_logger().info("rover_status_publisher node has started")

        self.battery_level = 50.0

        self.battery_publisher = self.create_publisher(Float32, "/rover/battery_status", 10)
        self.mode_publisher = self.create_publisher(String, "/rover/mode", 10)
        self.stop_publisher = self.create_publisher(Bool, "/rover/stop", 10)

        self.timer_ = self.create_timer(0.5, self.send_message)

    def send_message(self): 

        battery_msg = Float32()
        mode_msg = String()
        stop_msg = Bool()

        battery_msg.data = self.battery_level
        mode_msg.data = "Mode 1"
        stop_msg.data = False
        
        if self.battery_level > 0:

            self.battery_publisher.publish(battery_msg)
            self.battery_level -= 0.1

            self.mode_publisher.publish(mode_msg)

            self.stop_publisher.publish(stop_msg)

        else:

            self.battery_level = 0.0
            self.battery_publisher.publish(battery_msg)

            mode_msg.data = "Rover is out of battery"
            self.mode_publisher.publish(mode_msg)

            stop_msg.data = True
            self.stop_publisher.publish(stop_msg)

        
def main(args=None):
    
    rclpy.init(args=args)

    node=rover_status_publisher()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
        

        
        
        