# Its purpose is to hold the actions or 
# instructions that the launch system should perform
from launch import LaunchDescription, LaunchContext

# Joins multiple path parts to create a complete path
from launch.substitutions import PathJoinSubstitution, Command

"""
Command
→ Executes a command and gives its output to the launch system.

Purpose:
→ Useful when a launch file needs the result of an external command.
"""

# Finds the installed share directory of a ROS 2 package
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node 

# Explicitly tells ROS 2 what type a parameter value should be.
# In our case , URDF XML -> String -> robot_description parameter
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # Find the robot package's share directory
    robot_package_path = FindPackageShare("robot")

    # This is the ROS 2 launch object that joins path components
    robot_urdf_path = PathJoinSubstitution([
        robot_package_path,
        "urdf",
        "my_robot_model.xacro"
    ])

    robot_description = Command([
        "xacro ",
        robot_urdf_path
    ])
    
    # Evaluate/resolve the substitution and get its actual value
    print("Robot description:", robot_description.perform(LaunchContext()))

    robot_state_publisher_node = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        # Configuration values given to a ROS 2 node when it starts
        parameters = [
            {
                # Wrap this value and explicitly tell ROS 2 what type it should be
                "robot_description": ParameterValue(
                    robot_description,
                    value_type = str
                )
            }
        ],
        output = "screen"
    )
    print("Robot package path:", robot_package_path.perform(LaunchContext()))
    print("Robot URDF path:", robot_urdf_path.perform(LaunchContext()))

    return LaunchDescription([
        robot_state_publisher_node
    ])