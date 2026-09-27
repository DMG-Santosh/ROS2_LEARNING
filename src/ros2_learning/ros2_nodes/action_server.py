import rclpy
import time
from rclpy.node import Node

# ActionServer is the ROS 2 class that allows our node to provide an Action.
from rclpy.action import ActionServer, CancelResponse

# This imports the Action interface 
from example_interfaces.action import Fibonacci
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__("fibonacci_action_server")

        self.callback_group = ReentrantCallbackGroup()

        self.action_server = ActionServer(
            self,
            Fibonacci,
            "fibonacci",     # This is the Action name as, /fibonacci
            self.execute_callback,

            # If a client asks to cancel a Goal, call my cancel_callback() function
            cancel_callback = self.cancel_callback,

            callback_group = self.callback_group
        )

    

    def execute_callback(self, goal_handle):
        self.get_logger().info("Executing goal...")

        # Create an empty Feedback message.
        # We will use this object to send the current Fibonacci sequence
        # back to the Action Client while the calculation is running.

        feedback_msg = Fibonacci.Feedback()

        # Start the Fibonacci sequence with the first two numbers: 0 and 1.
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info("Goal canceled")
                return Fibonacci.Result()
            
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            )

            # Send the current Fibonacci sequence as Feedback
            # to the Action Client.
            
            # The client can therefore see the progress while the
            # Action is still running.

            
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        # Tell ROS 2 that the Action Goal has completed successfully.   
        goal_handle.succeed()

        # Create an empty Result message.
        # This will contain the final Fibonacci sequence.
        result = Fibonacci.Result()

        # Copy the completed Fibonacci sequence into the Result message.
        result.sequence = feedback_msg.sequence

        # Send the final Result back to the Action Client.
        return result


    # cancel_callback() receives a cancellation request and 
    # decides whether the Action Server should accept or reject it.
    def cancel_callback(self, goal_handle):
        self.get_logger().info("Cancel request received")
        return CancelResponse.ACCEPT


# "If somebody provides ROS 2 arguments,
# I can receive them. If nobody provides any, that's also okay."
def main(args=None):
    rclpy.init(args=args)

    node = FibonacciActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()