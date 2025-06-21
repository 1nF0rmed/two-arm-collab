import os
from dotenv import load_dotenv

from lerobot.common.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
from lerobot.common.robots.so101_follower import SO101FollowerConfig, SO101Follower

load_dotenv()

ROBOT_ID = os.getenv("ROBOT_ID")
ROBOT_PORT = os.getenv("ROBOT_PORT")

TELEOP_ID = os.getenv("TELEOP_ID")
TELEOP_PORT = os.getenv("TELEOP_PORT")

robot_config = SO101FollowerConfig(
    id=ROBOT_ID,
    port=ROBOT_PORT,
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
    action = teleop.get_action()
    robot.send_action(action)