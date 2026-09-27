import rclpy
from rclpy.node import Node
from ros2_custom_interfaces.srv import AddNumbers

class CustomServiceClient(Node):

    def __init__(self):
        super().__init__("custom_service_client")

        self.client = self.create_client(
            AddNumbers,
            "add_numbers"
        )
        while not self.client.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info("Waiting for service.....")

        # Create an empty request
        request = AddNumbers.Request()

        # Now we are putting the values
        request.a = 10
        request.b = 20

        # Send this request without stopping the program while waiting
        pending_response = self.client.call_async(request)
        pending_response.add_done_callback(self.response_callback)

    # The response callback is the function that handles the 
    # server's response after the request has been completed.
    def response_callback(self, pending_response):
        response = pending_response.result()
        self.get_logger().info(f"Result: {response.sum}")

def main(args = None):
    rclpy.init(args = args)
    node = CustomServiceClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()