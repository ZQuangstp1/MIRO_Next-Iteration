import rospy
import miro2 as miro
from flask import Flask
from flask_socketio import SocketIO
import os

# Initialize ROS Node
rospy.init_node("miro_bridge_server")

# Fetch Robot Name from Environment Variables (Default to 'miro' if not set)
robot_name = os.getenv("MIRO_ROBOT_NAME", "miro")
topic_base = "/" + robot_name

# Define the Publisher for kinematic control (movement)
pub_wheels = rospy.Publisher(topic_base + "/core/control/kinematic", 
                             miro2.msg.control_kinematic, queue_size=0)

# Initialize Flask-SocketIO to listen for commands from Node.js
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('move_command')
def handle_move(data):
    """
    Callback function triggered when a movement command is received via Socket.
    """
    linear = data.get('linear', 0)
    angular = data.get('angular', 0)
    
    # Create and publish the ROS message
    msg = miro2.msg.control_kinematic()
    msg.velocity.linear.x = linear
    msg.velocity.angular.z = angular
    pub_wheels.publish(msg)
    
    print(f"Executing Move: Linear={linear}, Angular={angular}")

if __name__ == '__main__':
    # Running on Port 5000 to avoid conflict with Node.js
    socketio.run(app, port=5000)
