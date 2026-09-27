import rclpy
from rclpy.node import Node
# Imports our custom AddNumbers Service interface.
from ros2_custom_interfaces.srv import AddNumbers

class CustomServiceServer(Node):

    def __init__(self):
                        # node name
        super().__init__("custom_service_server")

        self.service = self.create_service(
            # Use my custom AddNumbers.srv communication structure
            AddNumbers,
            # Service name
            "add_numbers",
            # When a client sends a request to /add_numbers, call this Python function
            self.add_numbers_callback
        )

    def add_numbers_callback(self, request, response):
        response.sum = request.a + request.b
        return response

# "args=None" allows ROS 2 command-line arguments to be passed into the program.
# If nobody gives args a value, use None by default
def main(args = None):
    # Passes the main() function's args value to rclpy.init()
    # left(args) = parameter, right(args) = variable
    rclpy.init(args = args)
    node = CustomServiceServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
