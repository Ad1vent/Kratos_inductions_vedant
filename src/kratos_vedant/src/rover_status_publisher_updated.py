#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import kratos_vedant_msgs
from kratos_vedant_msgs.msg import RoverStatus

class rover_status_publisher(Node):

    def __init__(self):

        super().__init__("rover_status_publisher")
        self.get_logger().info("rover_status_publisher node has started")

        self.battery_level = 50.0

        self.status_publisher = self.create_publisher(RoverStatus, "/rover/status", 10)

        #frequency = 1/T therefore for 2Hz it should be 0.5sec
        self.timer_ = self.create_timer(0.5, self.send_message)

    def send_message(self): 

        msg = RoverStatus()

        msg.battery_percentage = self.battery_level
        msg.mode = "Mode 1"
        msg.emergency_stop = False

        
        if self.battery_level > 0:

            self.status_publisher.publish(msg)
            self.battery_level -= 0.1

        else:

            self.battery_level = 0.0
            msg.mode = "Rover is out of battery"
            msg.emergency_stop = True

            self.status_publisher.publish(msg)




        
def main(args=None):
    
    rclpy.init(args=args)

    node=rover_status_publisher()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
        

        
        
        