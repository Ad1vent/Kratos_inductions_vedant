#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
from math import atan2, atan, sqrt, sin, cos, acos
import geometry_msgs
from geometry_msgs.msg import Point


class IKController (Node):

    def __init__(self):

        super().__init__('ik_controller')

        self.msg_publisher = self.create_publisher(JointState, '/joint_states', 10)

        self.end = Point()

        self.shoulder_joint_angle = 0.0
        self.elbow_joint_angle = 0.0
        self.base_yaw_joint_angle = 0.0

        self.shoulder_length=2
        self.forearm_length=3

        self.timer_ = self.create_timer(3, self.send_message)


    def send_message(self):

        axis=input("Enter the axis to move along (x|y|z):").lower()
        while (axis not in ['x', 'y', 'z']):

            print("Invalid axis selection")
            axis = input("Enter the axis to move along (x|y|z): ").lower()


        distance=float(input("Enter the distance to move along axis:"))
        self.add_distance(axis, distance)

        msg = JointState()

        msg.header.stamp = self.get_clock().now().to_msg() #Note: what does this do
        msg.name = ["base_yaw_joint","shoulder_joint","elbow_joint"]
        msg.position = [self.base_yaw_joint_angle, self.shoulder_joint_angle, self.elbow_joint_angle]

        self.msg_publisher.publish(msg)

            
    def add_distance(self, axis, distance):

        x_pos=self.end.x
        y_pos=self.end.y
        z_pos=self.end.z
        #creating a quicksave

        if (axis=='x'):
            self.end.x+=distance

        elif (axis=='y'):
            self.end.y+=distance

        else:
            self.end.z+=distance

        l2 = self.shoulder_length 
        l3 = self.forearm_length

        dist=sqrt(self.end.x**2 + self.end.y**2 + self.end.z**2)

        if (dist > l2+l3 or dist<l3-l2):

            #Note: add a future boundary for y>=0

            self.get_logger().info("Final position is beyond arm reach")

            #reloading last saved pos and angles
            self.end.x = x_pos
            self.end.y = y_pos
            self.end.z = z_pos
            
        else: 

            self.inv_kine()

            self.get_logger().info("New joint angles:")
            self.get_logger().info(f"Base: {self.base_yaw_joint_angle:f}")
            self.get_logger().info(f"Shoulder: {self.shoulder_joint_angle:f}")
            self.get_logger().info(f"Elbow: {self.elbow_joint_angle:f}")
            
            
      


    def inv_kine(self):

            r=sqrt(self.end.y**2 + self.end.x**2)
            l2 = self.shoulder_length
            l3 = self.forearm_length

            #we are now in the yz plane ( along the base vector r=sqrt(x^2+y^2) )
            # this now forms a 2d planar arm with lengths L2 and L3 (shoulder length and forearm length)

            #let us take the 2nd angle to always be NEGATIVE (angle between L2 and L3)

            self.base_yaw_joint_angle = atan2(self.end.y, self.end.x)
            self.elbow_joint_angle = -1*acos((r**2 - l2**2 - l3**2)/(2*l2*l3))

            q3 = self.elbow_joint_angle #notation for the next formula

            self.shoulder_joint_angle= atan2(self.end.z, r) + atan2(l3*sin(q3), l2 + l3*cos(q3))

            


def main(args=None):

    rclpy.init(args=args)

    node = IKController()
    rclpy.spin(node)

    rclpy.shutdown()


if (__name__ == "__main__"):
    main()

