from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # =========================================================
    # PROCESS XACRO
    # =========================================================

    robot_description = ParameterValue(
        Command([
            "xacro ",
            PathJoinSubstitution([
                FindPackageShare("robot"),
                "urdf",
                "my_robot_model.xacro"
            ])
        ]),
        value_type=str
    )


    # =========================================================
    # ROBOT STATE PUBLISHER
    # =========================================================

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description
            }
        ]
    )


    # =========================================================
    # JOINT STATE PUBLISHER GUI
    # =========================================================

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen"
    )


    # =========================================================
    # LAUNCH DESCRIPTION
    # =========================================================

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node
    ])