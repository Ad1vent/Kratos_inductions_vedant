#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

import math  #for sqrt function

class DoubleAckermannController(Node):
    def __init__(self):
        super().__init__('double_ackermann_controller')
        
        # Subscribe to teleop/joystick commands
        self.cmd_sub = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_callback, 
            10
        )

        # Publisher for the 4 steering hinges (Position in Radians)
        # Order matches YAML: [fl_steer, fr_steer, rl_steer, rr_steer]
        self.steer_pub = self.create_publisher(
            Float64MultiArray, 
            '/steering_controller/commands', 
            10
        )

        # Publisher for the 4 wheel axles (Velocity in Rad/s)
        # Order matches YAML: [fl_drive, fr_drive, rl_drive, rr_drive]
        self.drive_pub = self.create_publisher(
            Float64MultiArray, 
            '/drive_controller/commands', 
            10
        )

        # Rover Physical Constants
        self.wheelbase = 0.4
        self.track_width = 0.6
        self.wheel_radius = 0.12

        self.get_logger().info("Double Ackermann Controller Node Started. Waiting for /cmd_vel...")

    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # =======================================================
        # APPLICANT TASK: Implement Double Ackermann Kinematics 
        # Calculate the 4 steering angles and 4 wheel velocities
        # =======================================================


    def cmd_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        fl_angle, fr_angle, rl_angle, rr_angle = 0.0, 0.0, 0.0, 0.0
        fl_vel, fr_vel, rl_vel, rr_vel = 0.0, 0.0, 0.0, 0.0

        #Note: the orientation of the rover is assumed to be pointing towards the +x axis, 
        # with its geometric centre located at 0,0

        if abs(angular_z) >= 0.001: # Case 1: angular_z != 0

            COR_y = linear_x / angular_z #centre of rotation (V/W=R)

            fl_angle = math.atan((self.wheelbase / 2.0) / (COR_y - (self.track_width / 2.0))) 
            fr_angle = math.atan((self.wheelbase / 2.0) / (COR_y + (self.track_width / 2.0)))

            #calculations for the above are attached in a picture 
            
            rl_angle = -fl_angle #due to symmetry of COR from both wheel ends
            rr_angle = -fr_angle


            #calculating distances of FL, RL (r_l) and FR, RR (r_r) from COR
            r_l = math.sqrt((self.wheelbase / 2.0)**2 + (COR_y - (self.track_width / 2.0))**2)
            r_r = math.sqrt((self.wheelbase / 2.0)**2 + (COR_y + (self.track_width / 2.0))**2)

            
            if abs(linear_x) >= 0.001: # Normal driving

                lhs_linear_velo = linear_x / math.cos(fl_angle) #vx/cos(theta)=v_linear_net
                rhs_linear_velo = linear_x / math.cos(fr_angle)

            #however, the cos theta method DOES NOT WORK when we have linear x=0, z!=0
            # because linear_x/cos(theta) = 0 when lin_x=0, therefore the rover will 
            # NOT spin in place, as opposed to using V(lin) = R.W (where W is angular z) 

            #I now realize we can probably use V=RW for any nonzero ang(Z) :(
            
            else: #in-place spinning (linear_x = 0)

                lhs_linear_velo = -angular_z * r_l #v_linear = r(wheel)*w(wheel) we use this...
                rhs_linear_velo = angular_z * r_r #... to derive w


            fl_vel = lhs_linear_velo / self.wheel_radius #v=rw
            fr_vel = rhs_linear_velo / self.wheel_radius

            rl_vel = fl_vel #since lhs/rhs wheels both move in same dirn(cw/acw), ...
            rr_vel = fr_vel #...they have the same speed (in radians)

        
        else: # Case 2: angular_z == 0 (rover moves straight)

            fl_angle = fr_angle = rl_angle = rr_angle = 0.0

            fl_vel = fr_vel = rl_vel = rr_vel = (linear_x / self.wheel_radius)


        # =======================================================
        
        # Publish Steering Commands
        steer_msg = Float64MultiArray()
        steer_msg.data = [fl_angle, fr_angle, rl_angle, rr_angle]
        self.steer_pub.publish(steer_msg)

        # Publish Drive Commands
        drive_msg = Float64MultiArray()
        drive_msg.data = [fl_vel, fr_vel, rl_vel, rr_vel]
        self.drive_pub.publish(drive_msg)




def main(args=None):
    rclpy.init(args=args)
    node = DoubleAckermannController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
