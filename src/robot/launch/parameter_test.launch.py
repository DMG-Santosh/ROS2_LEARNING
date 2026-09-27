# This import is necessary to use the launch instructions
from launch import LaunchDescription 
# This import is useful to create a node
from launch_ros.actions import Node

def generate_launch_description():

    # Creating a launch insruction for robot_state_publisher
    robot_state_publisher_node = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        parameters =[
            {
                "use_sim_time": False
            }
        ],
        output = "screen" 
    )

    return LaunchDescription([
        robot_state_publisher_node
    ])

