import os
from dotenv import load_dotenv

from lerobot.common.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.common.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower

load_dotenv()

ROBOT_ID = os.getenv("ROBOT_ID")
ROBOT_PORT = os.getenv("ROBOT_PORT")

TELEOP_ID = os.getenv("TELEOP_ID")
TELEOP_PORT = os.getenv("TELEOP_PORT")

WRIST_CAMERA_INDEX = int(os.getenv("WRIST_CAMERA_INDEX"))
TOP_CAMERA_INDEX = int(os.getenv("TOP_CAMERA_INDEX"))

camera_config = {
    "wrist": OpenCVCameraConfig(index_or_path=WRIST_CAMERA_INDEX, width=640, height=480, fps=30),
    "top": OpenCVCameraConfig(index_or_path=TOP_CAMERA_INDEX, width=640, height=480, fps=30),
}

robot_config = SO101FollowerConfig(
    id=ROBOT_ID,
    port=ROBOT_PORT,
    cameras=camera_config,
)

teleop_config = SO101LeaderConfig(
    id=TELEOP_ID,
    port=TELEOP_PORT
)

robot = SO101Follower(robot_config)
teleop = SO101Leader(teleop_config)

robot.connect()
teleop.connect()

while True:
    observation = robot.get_observation()
    action = teleop.get_action()
    robot.send_action(action)