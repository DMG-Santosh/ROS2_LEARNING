import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from ros2_custom_interfaces.action import SimpleCounter

class CustomActionServer(Node):

    def __init__(self):
        super().__init__("custom_action_server")

        self.action_server = ActionServer(
            self,
            SimpleCounter,
            "simple_counter",
            self.execute_callback
        )

    def execute_callback(self, goal_handle):

        # Give me the target value from the Goal 
        # that this Action Server is currently executing
        target = goal_handle.request.target

        # Create the Result object
        result = SimpleCounter.Result()

        # Create the Feedback object
        feedback = SimpleCounter.Feedback()

        # Create a counter loop
        for count in range(1, target + 1):
            feedback.current_count = count

            # sends the current Feedback to the Action Client
            goal_handle.publish_feedback(feedback)
            time.sleep(1)
        # This prepares the final answer that will be returned to the Client
        result.final_count = target
        # The requested Action has completed successfully
        goal_handle.succeed()
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = CustomActionServer()
    rclpy.spin(action_server)
    action_server.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()


