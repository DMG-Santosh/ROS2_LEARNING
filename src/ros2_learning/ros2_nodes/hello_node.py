# loads ROS Python support into the file(ROS Client Library for Python)
import rclpy 

# Imports the ROS Node class into the program that allows us to create our own nodes
from rclpy.node import Node

# To send text messages
from std_msgs.msg import String

class HelloNode(Node):
    def __init__(self):
        # This line initializes the parent Node class and gives your ROS node a name ("hello_node")
        super().__init__("hello_node")

        # Creates a Publisher object that can publish String messages to the topic:
        self.publisher_ = self.create_publisher(String, "chatter", 10)

        # Creates a timer that runs every 1 second.
        self.timer = self.create_timer(1.0, self.timer_callback)

        # This line prints a message using the ROS logging system.
        # self.get_logger().info("Hello ROS2")

    def timer_callback(self):
        # Creates an empty ROS String message.
        msg = String()

        # Stores the text inside the ROS message.
        msg.data = "Hello ROS2"

        # This line sends the message to the Topic.
        self.publisher_.publish(msg)

        # Prints every published message in the terminal.
        self.get_logger().info(f"Publishing: {msg.data}")

def main():
    # This line starts the ROS 2 Python client library.
    rclpy.init()

    # creates an actual object of your HelloNode class.
    node = HelloNode()

    # Keep this node running and continuously listen for ROS events.
    rclpy.spin(node)

    # This line destroys (removes) the node from the ROS system
    node.destroy_node() 

    # This line shuts down the ROS 2 client library.
    rclpy.shutdown()

if __name__ == "__main__":
    main()