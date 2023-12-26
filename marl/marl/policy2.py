import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# Preamble
import numpy as np
import time


class policy2(Node):
    def __init__(self):
        super().__init__('policy2')
        self.publisher_ = self.create_publisher(
            Image, 'policy_topic2', 10)
        self.subscription = self.create_subscription(
            Image,
            'env_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        received_np_array = msg.data
        time.sleep(0.5)
        self.send_message(msg.data)

    def send_message(self, val):
        msg = Image()
        # Assuming self.state is a 2D array, we need to convert it to a 1D array for Image
        msg.data = val.tobytes()
        # You will need to set height, width, and encoding correctly
        msg.height = 50
        msg.width = 50
        msg.encoding = '32FC1'  # For a single-channel 32-bit float
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    policy_node = policy2()
    rclpy.spin(policy_node)
    policy_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
