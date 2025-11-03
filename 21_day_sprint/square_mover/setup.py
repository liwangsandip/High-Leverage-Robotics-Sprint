from setuptools import find_packages, setup

package_name = 'square_mover'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sandip',
    maintainer_email='sandeeplimbu113@gmail.com',
    description='ROS 2 package for Project 1: Autonomous Square',
    license='TODO: License declaration',
    tests_require=['pytest'],
    # --- IMPORTANT ENTRY POINT BELOW ---
    entry_points={
        'console_scripts': [
            # This line registers your Python script as a runnable ROS 2 node
            'autonomous_square = square_mover.autonomous_square:main',
        ],
    },
)
