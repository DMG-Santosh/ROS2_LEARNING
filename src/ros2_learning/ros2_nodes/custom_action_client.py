import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from ros2_custom_interfaces.action import SimpleCounter

class CustomActionClient(Node):
        
    def __init__(self):
        super().__init__("custom_action_client")    

        self.action_client = ActionClient(
            self,
            SimpleCounter,
            "simple_counter"
        )

        self.action_client.wait_for_server()

        # Creates an empty goal object
        goal = SimpleCounter.Goal()

        # Count until the target
        goal.target = 5
        # Waiting for the response to our Goal request.
        pending_goal = self.action_client.send_goal_async(
            goal,
            feedback_callback = self.feedback_callback
            )

        # When the pending Goal response is ready, 
        # call my goal_response_callback() function
        pending_goal.add_done_callback(self.goal_response_callback)

    # Create a function that will run when the Goal response is ready
    def goal_response_callback(self, pending_goal):
        # Gets the actual Goal response from the completed pending response
        goal_handle = pending_goal.result()

        if not goal_handle.accepted:
            self.getlogger().info("Goal rejected")
            return
        
        # Start waiting asynchronously for the final Result and 
        # store the pending operation in pending_result
        pending_result = goal_handle.get_result_async()

        # When the final Action Result becomes available, 
        # call my result_callback() function
        pending_result.add_done_callback(self.result_callback)

    def result_callback(self, pending_result):

        # First get the completed response, 
        # then access the actual "SimpleCounter.Result" contained inside it.

        """
        pending_result
            ↓
        .result()       ← method: get completed response
            ↓
        response object
            ↓
        .result         ← property: get actual Action Result
            ↓
        SimpleCounter.Result
        """
        result = pending_result.result().result

        # Extracts the final_count value from the custom Action Result
        final_count = result.final_count
        self.get_logger().info(f"Final count: {final_count}")

    def feedback_callback(self,feedback_message):

        # The feedback_message is the message ROS 2 gives our callback.
        # It contains the Feedback information from the Action.
        # Give me the actual Feedback data from this received message
        feedback = feedback_message.feedback

        # Gets the current_count value defined in our custom .action file
        current_count = feedback.current_count
        self.get_logger().info(f"Current count: {current_count}")

def main(args=None):
    rclpy.init(args=args)
    action_client = CustomActionClient()

    # Keeps the Node running so ROS 2 can process callbacks, Feedback, and Result
    rclpy.spin(action_client)
    action_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


        

    

