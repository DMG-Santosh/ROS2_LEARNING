import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):

    def __init__(self):
        super().__init__("service_client")

        self.add_service = self.create_client(
            AddTwoInts,
            "add_two_ints"
        )

        """
        Checks the Service Server available or not every "1" second
        and "not" reverses the Boolean result 
        so that the loop continues while the service is unavailable.

        """
        while not self.add_service.wait_for_service(timeout_sec = 1.0):
            self.get_logger().info("Waiting for service.....")

        # Creates a Request object using the AddTwoInts service interface.
        self.request = AddTwoInts.Request()

        # Now the request data is ready
        self.request.a = 5
        self.request.b = 3

        """
        "call_async()" means Send this request to the Service Server 
         without blocking the Client while waiting for the response.
        
        """        
        self.pending_response = self.add_service.call_async(self.request)

        """
        "add_done_callback()" allows the Client to handle the response 
        when it becomes available, instead of continuously checking for it.
        
        """
        self.pending_response.add_done_callback(self.response_callback)

    def response_callback(self, pending_response):
        response = pending_response.result()
        self.get_logger().info(f"Result: {response.sum}")


def main():
    rclpy.init()
    node = ServiceClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()