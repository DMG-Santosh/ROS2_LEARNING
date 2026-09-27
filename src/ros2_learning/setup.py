from setuptools import find_packages, setup

package_name = 'ros2_learning'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (
        'share/ament_index/resource_index/packages',
        ['resource/' + package_name]
    ),
    (
        'share/' + package_name,
        ['package.xml']
    ),
    (
        'share/' + package_name + '/config',
        ['config/parameter.yaml',
         'config/robot_2.yaml'

        ]
    ),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='santosh',
    maintainer_email='santosh@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={

        # Syntax
        # 'executable_name = package_name.python_file:main',
        
        'console_scripts': [
            'hello_node = ros2_nodes.hello_node:main',
            'subscriber_node = ros2_nodes.subscriber_node:main',
            'service_server = ros2_nodes.service_server:main',
            'service_client = ros2_nodes.service_client:main',
            'parameter_node = ros2_nodes.parameter_node:main',
            'action_server = ros2_nodes.action_server:main',
            'action_client = ros2_nodes.action_client:main',
            'custom_service_server = ros2_nodes.custom_service_server:main',
            'custom_service_client = ros2_nodes.custom_service_client:main',
            'custom_action_server = ros2_nodes.custom_action_server:main',
            'custom_action_client = ros2_nodes.custom_action_client:main',
        ],
    },
)
