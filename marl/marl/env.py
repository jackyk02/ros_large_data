import time
import rclpy
from rclpy.node import Node
from message_filters import TimeSynchronizer, Subscriber
import numpy as np
from sensor_msgs.msg import Image


class Env(Node):
    def __init__(self):
        super().__init__('env')

        # Subscribers
        self.policy1 = Subscriber(self, Image, 'policy_topic1')
        self.policy2 = Subscriber(self, Image, 'policy_topic2')
        self.policy3 = Subscriber(self, Image, 'policy_topic3')
        self.policy4 = Subscriber(self, Image, 'policy_topic4')

        # Synchronize the subscribers
        ats = TimeSynchronizer(
            [self.policy1, self.policy2, self.policy3, self.policy4], 10)
        ats.registerCallback(self.callback)

        # Publisher
        self.publisher = self.create_publisher(
            Image, 'env_topic', 10)

        # Simulation
        self.round_num = 0
        self.start_time = None

        # Create the 2D NumPy array
        self.val = np.zeros(13107200)

        self.send_message()

    def callback(self, p1, p2, p3, p4):

        # first round
        if int(self.round_num) == 0:
            self.start_time = time.time()

        # print round number
        print("Episode: "+str(self.round_num))
        self.round_num += 1

        # print Time Taken
        print(f"Time taken: {time.time() - self.start_time:.2f} seconds")

        self.send_message()

    def send_message(self):
        msg = Image()
        # Assuming self.state is a 2D array, we need to convert it to a 1D array for Image
        msg.data = self.val.tobytes()
        # You will need to set height, width, and encoding correctly
        msg.height = 50
        msg.width = 50
        msg.encoding = '32FC1'  # For a single-channel 32-bit float
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    env_node = Env()
    rclpy.spin(env_node)
    env_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
