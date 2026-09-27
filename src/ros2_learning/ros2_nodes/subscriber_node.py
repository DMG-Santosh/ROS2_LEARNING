import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Creates a new ROS node class
class SubscriberNode(Node):

    def __init__(self):
        # This line initializes the parent Node class and gives your ROS node a name ("subscriber_node")
        super().__init__("subscriber_node")

        # Creates a Subscriber that listens to the topic /chatter
        self.subscription = self.create_subscription(
            String,
            "chatter",
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # Processes every message received from the subscribed topic
        self.get_logger().info(f"Received: {msg.data}")

def main():
    rclpy.init()
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
