# autonomous_square.py

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Define the constants for movement
LINEAR_SPEED = 0.1  # m/s (Adjust this carefully!)
ANGULAR_SPEED = 0.5 # rad/s
TURN_DURATION = 1.5 # seconds to turn 90 degrees (rough estimate)
MOVE_DURATION = 5.0 # seconds to move straight

class AutonomousSquare(Node):
    def __init__(self):
        super().__init__('autonomous_square_node')
        
        # 1. Setup Publisher for movement commands
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', qos_profile)
        self.publisher_.publish(Twist())
        self.get_logger().info('Published initial stop command.')
        
        self.get_logger().info('AutonomousSquare node started. Waiting for command...')
        
        # Initialize state variables
        self.state = 'FORWARD'
        self.timer = None
        self.twist_msg = Twist()
        
        # Start the movement loop
        self.start_movement_loop()

    def start_movement_loop(self):
        # The core timer that drives the state machine
        self.timer = self.create_timer(0.05, self.movement_callback)
        self.next_transition_time = self.get_clock().now().nanoseconds / 1e9 + MOVE_DURATION

    def movement_callback(self):
        # *** DAY 6 LOGIC GOES HERE (Obstacle Avoidance) ***
        # We will add sensor reading logic here later to check for walls.

        current_time = self.get_clock().now().nanoseconds / 1e9
        
        # State Machine Logic
        if self.state == 'FORWARD':
            if current_time >= self.next_transition_time:
                # Transition to turning state
                self.state = 'TURN'
                self.next_transition_time = current_time + TURN_DURATION
                self.get_logger().info('Transition: Starting Turn')
                
                self.twist_msg.linear.x = 0.0
                self.twist_msg.angular.z = ANGULAR_SPEED
            else:
                # Continue moving forward
                self.twist_msg.linear.x = LINEAR_SPEED
                self.twist_msg.angular.z = 0.0

        elif self.state == 'TURN':
            if current_time >= self.next_transition_time:
                # Transition back to forward state
                self.state = 'FORWARD'
                self.next_transition_time = current_time + MOVE_DURATION
                self.get_logger().info('Transition: Starting Forward')

                self.twist_msg.linear.x = LINEAR_SPEED
                self.twist_msg.angular.z = 0.0
            else:
                # Continue turning
                self.twist_msg.linear.x = 0.0
                self.twist_msg.angular.z = ANGULAR_SPEED
        
        # Publish the command
        self.publisher_.publish(self.twist_msg)

    def destroy_node(self):
        # Stop the robot when the node shuts down
        self.twist_msg.linear.x = 0.0
        self.twist_msg.angular.z = 0.0
        self.publisher_.publish(self.twist_msg)
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    autonomous_square = AutonomousSquare()
    rclpy.spin(autonomous_square)
    autonomous_square.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
