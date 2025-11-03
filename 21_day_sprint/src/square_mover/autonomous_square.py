import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
# Added for LiDAR
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
import math # Added for handling inf values in LiDAR data

# Define the constants for movement
LINEAR_SPEED = 0.1  # m/s
ANGULAR_SPEED = 0.5 # rad/s
TURN_DURATION = 1.5 # seconds to turn 90 degrees (rough estimate)
MOVE_DURATION = 5.0 # seconds to move straight
# Safety distance for obstacle avoidance (we'll use this later)
SAFE_DISTANCE = 0.35 # meters

class AutonomousSquare(Node):
    def __init__(self):
        super().__init__('autonomous_square_node')

        # 1. Setup QoS Profile (Reliable for Gazebo)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # 2. Setup Publisher (Movement) and Subscriber (LiDAR)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', qos_profile)
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile
        )
        self.get_logger().info('LiDAR Subscriber initialized.')

        # 3. Initialize State Variables
        self.state = 'FORWARD'
        self.timer = None
        self.twist_msg = Twist()
        self.min_distance = 10.0 # Variable to store the closest obstacle distance

        # 4. Stabilization and Start
        self.publisher_.publish(Twist()) # Send initial stop command (Stabilization Fix)
        self.get_logger().info('AutonomousSquare node started. Waiting for command...')
        self.start_movement_loop()

    def start_movement_loop(self):
        # The core timer that drives the state machine
        self.timer = self.create_timer(0.05, self.movement_callback) # Frequency Fix (0.05s)
        self.next_transition_time = self.get_clock().now().nanoseconds / 1e9 + MOVE_DURATION

    def scan_callback(self, msg):
        """
        Processes incoming LaserScan messages to find the minimum distance.
        This runs every time a new LiDAR message is received (~10-15 times per second).
        """
        # The 'ranges' array contains distance measurements (0.0 to inf).
        
        try:
            # Filter out 'inf' (unbounded distance) and 0.0 values (sensor error), then find the minimum
            # This logic finds the closest obstacle in any direction.
            valid_ranges = [r for r in msg.ranges if r > 0.01 and not math.isinf(r)]
            
            if valid_ranges:
                self.min_distance = min(valid_ranges)
            else:
                self.min_distance = 10.0 # Default safe value if no valid data
        except Exception as e:
            self.get_logger().error(f"Error processing scan data: {e}")
            self.min_distance = 10.0
            
        # IMPORTANT: Uncomment the line below to check if the LiDAR is working correctly!
        self.get_logger().info(f"Closest obstacle distance: {self.min_distance:.2f} m")

    def movement_callback(self):
        """
        The main control loop that switches between FORWARD and TURN states.
        """
        current_time = self.get_clock().now().nanoseconds / 1e9

        # Reset velocity commands for the current step
        self.twist_msg.linear.x = 0.0
        self.twist_msg.angular.z = 0.0

        if self.state == 'FORWARD':
            # Check if it's time to turn
            if current_time >= self.next_transition_time:
                self.state = 'TURN'
                self.next_transition_time = current_time + TURN_DURATION
                self.get_logger().info('Transition: Starting Turn')
            # Otherwise, keep moving forward
            else:
                self.twist_msg.linear.x = LINEAR_SPEED

        elif self.state == 'TURN':
            # Check if it's time to move forward
            if current_time >= self.next_transition_time:
                self.state = 'FORWARD'
                self.next_transition_time = current_time + MOVE_DURATION
                self.get_logger().info('Transition: Starting Forward')
            # Otherwise, keep turning
            else:
                self.twist_msg.angular.z = ANGULAR_SPEED

        # Publish the command determined by the current state
        self.publisher_.publish(self.twist_msg)


def main(args=None):
    rclpy.init(args=args)
    autonomous_square = AutonomousSquare()
    rclpy.spin(autonomous_square)
    autonomous_square.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
