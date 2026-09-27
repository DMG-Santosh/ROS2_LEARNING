import rclpy
from rclpy.node import Node

# Importing predefined ROS2 Service type called "AddTwoInts"
from example_interfaces.srv import AddTwoInts

class ServiceServer(Node):

    def __init__(self):

        # Initializes the ROS Node and the node name is "service_server"
        super().__init__("service_server")

        # Creates a ROS2 Service Server
        self.add_service = self.create_service(
            
            # Service Type(Also called a Service Interface)
            AddTwoInts,

            # This is the service name
            "add_two_ints",

            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):

        # a, b, and sum are fields defined by the AddTwoInts service interface
        response.sum = request.a + request.b

        # Adding a logger to see the output in terminal
        self.get_logger().info(
            f"Request: {request.a} + {request.b} = {response.sum}"
        )

        return response


def main():
    rclpy.init()
    node = ServiceServer()
    rclpy.spin(node)
    # Remove this particular ROS node.
    node.destroy_node()
    # Shut down the ROS 2 Python client library for this Python program.
    rclpy.shutdown()

if __name__ == "__main__":
    main()