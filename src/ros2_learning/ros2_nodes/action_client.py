import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__("fibonacci_action_client")

        self.action_client = ActionClient(
            self, 
            Fibonacci,
            "fibonacci"
        )

        # Don't continue until the /fibonacci Action Server is available
        self.action_client.wait_for_server()

        # Create an empty Goal
        goal_msg = Fibonacci.Goal()
        # Put our requested value into the Goal
        goal_msg.order = 5

        self.send_goal = self.action_client.send_goal_async(
            goal_msg,

            # Whenever Feedback arrives from the Action Server, 
            # call my feedback_callback() function.
            feedback_callback = self.feedback_callback
        )

        # When the Goal response is ready → call goal_response_callback()
        self.send_goal.add_done_callback(self.goal_response_callback)

    # "feedback_msg" (It is received from the server)
    def feedback_callback(self, feedback_msg):

        # Take the actual Feedback data out of the received ROS 2 message
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f"Feedback: {feedback.sequence}"
        )

    # This function will be called when ROS 2 knows whether 
    # the server accepted our Goal
    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return
        
        self.get_logger().info("Goal accepted")

        self.get_result_future = goal_handle.get_result_async()

        # When the Result is ready → call get_result_callback()
        self.get_result_future.add_done_callback(self.get_result_callback)

    # This function will be called when the final Result becomes available
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f"Result: {result.sequence}"
        )

def main(args = None):
    rclpy.init(args = args)
    node = FibonacciActionClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

