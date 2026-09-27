import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult

class ParameterNode(Node):

    def __init__(self):

        super().__init__("parameter_node")

        # PARAMETER DECLARATION Syntax
        # self.declare_parameter("parameter_name", default_value)

        # Used to declare/register a parameter for a ROS 2 node(Integer parameter)
        self.declare_parameter("my_number", 10)

        # Float parameter (But in CLI ROS considers as double) 
        self.declare_parameter("my_speed", 2.5)

        # String parameter
        self.declare_parameter("robot_name", "My_Robot")

        # Boolean parameter
        self.declare_parameter("robot_enabled", True)

        # Get parameter values
        self.my_number = self.get_parameter("my_number").value
        self.my_speed = self.get_parameter("my_speed").value
        self.robot_name = self.get_parameter("robot_name").value
        self.robot_enabled = self.get_parameter("robot_enabled").value


       
        # Print parameter values
        self.get_logger().info(
            f"Number: {self.my_number}"
        )

        self.get_logger().info(
            f"Speed: {self.my_speed}"
        )

        self.get_logger().info(
            f"Robot Name: {self.robot_name}"
        )

        self.get_logger().info(
            f"Robot Enabled: {self.robot_enabled}"
        )

        # Register parameter callback
        self.add_on_set_parameters_callback(
            self.parameter_callback
        )


    def parameter_callback(self, parameters):

        for parameter in parameters:

            if parameter.name == "my_number":
                self.my_number = parameter.value

                self.get_logger().info(
                    f"Parameter changed: {parameter.name} = {parameter.value}"
                )

                return SetParametersResult(successful = True)

            else:
                self.get_logger().warn(
                    "my_number must be 0 or greater"
                )

                return SetParametersResult(successful=False)

        return SetParametersResult(successful=True)



def main():
    rclpy.init()
    node = ParameterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()