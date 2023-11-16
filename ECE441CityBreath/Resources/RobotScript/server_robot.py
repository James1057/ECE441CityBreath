#!/usr/bin/env python3
# coding=utf8

import sys
import math
import rospy
from std_srvs.srv import SetBool
from puppy_control.msg import Velocity, Pose, Gait
import socket
import time

ROS_NODE_NAME = 'puppy_demo'

PuppyMove = {'x': 0, 'y': 0, 'yaw_rate': 0}  # Initialize movement parameters

PuppyPose = {'roll': math.radians(0), 'pitch': math.radians(0), 'yaw': 0.000, 'height': -10, 'x_shift': 0.5, 'stance_x': 0, 'stance_y': 0}

#PuppyMove = {'x':6, 'y':0, 'yaw_rate':0} # Move to go straight
#PuppyMove = {'x':6, 'y':0, 'yaw_rate':0.18} # turn counterclockwise to go 10 degres per second
#PuppyPose = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':0.5, 'stance_x':0, 'stance_y':0}
# PuppyPose = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}

print('The Server is being started')

# Replace with the server's IP address and port
SERVER_IP = '0.0.0.0'
SERVER_PORT = 2131

# Define functions

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

gait = 'Walk'
# Choose gait between trot, Amble, and Walk

if gait == 'Trot':
    GaitConfig = {'overlap_time': 0.2, 'swing_time': 0.3, 'clearance_time': 0.0, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.65

elif gait == 'Amble':
    GaitConfig = {'overlap_time': 0.1, 'swing_time': 0.2, 'clearance_time': 0.1, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.9

elif gait == 'Walk':
    GaitConfig = {'overlap_time': 0.1, 'swing_time': 0.2, 'clearance_time': 0.3, 'z_clearance': 5}
    PuppyPose['x_shift'] = -0.65

def cleanup():
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    print('Puppy movement stopped')

# New function to control puppy's movement
def move_puppy(x, y, yaw_rate):
    # Publish the puppy's movement command
    PuppyVelocityPub.publish(x=x, y=y, yaw_rate=yaw_rate)

def main():
    hold = ""
    while True:
        try:
        # Create a socket to listen for incoming connections
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((SERVER_IP, SERVER_PORT))
            server_socket.listen(1)

            print(f"Listening for connections on {SERVER_IP}:{SERVER_PORT}")
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            try:
                #while True:
                key = client_socket.recv(1).decode()
                print(f"Received key: {key}")
                client_socket.close()
                server_socket.close()
                if hold != key:
                    if key == 'w':
                        # Call the move_puppy function to make the puppy walk forward
                        move_puppy(6, 0, 0)  # Adjust the parameters as needed
                    elif key == 's':
                        # Call the move_puppy function to make the puppy walk backward
                        move_puppy(-6, 0, 0)  # Adjust the parameters as needed
                    elif key == 'a':
                        # Call the move_puppy function to make the puppy walk left
                        move_puppy(6, 0,0.18)  # Adjust the parameters as  
                    elif key == 'd':
                        # Call the move_puppy function to make the puppy walk right
                        move_puppy(6, 0,-0.18)  # Adjust the parameters as needed
                    elif key == 'e':
                        # Stop puppy movement and run cleanup
                        cleanup()
                    elif key == 'q':
                        exit()
                    hold = key

            except KeyboardInterrupt:
                pass
            
            client_socket.close()
            server_socket.close()

            time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    rospy.init_node(ROS_NODE_NAME, log_level=rospy.INFO)
    rospy.on_shutdown(cleanup)

    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    PuppyGaitConfigPub = rospy.Publisher('/puppy_control/gait', Gait, queue_size=1)
    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)

    set_mark_time_srv = rospy.ServiceProxy('/puppy_control/set_mark_time', SetBool)

    rospy.sleep(0.2)
    PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'], height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time=500)

    rospy.sleep(0.2)
    PuppyGaitConfigPub.publish(overlap_time=GaitConfig['overlap_time'], swing_time=GaitConfig['swing_time'], clearance_time=GaitConfig['clearance_time'], z_clearance=GaitConfig['z_clearance'])

    main()
