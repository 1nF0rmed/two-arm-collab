import argparse
import os
from dotenv import load_dotenv

import numpy as np
import rerun as rr
from lerobot.common.utils.utils import log_say
from lerobot.common.utils.control_utils import init_keyboard_listener
from lerobot.common.utils.visualization_utils import _init_rerun
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

def teleop():
    robot = SO101Follower(robot_config)
    teleop = SO101Leader(teleop_config)

    robot.connect()
    teleop.connect()

    _init_rerun(session_name="teleoperate_pick_up_box")

    listener, events = init_keyboard_listener()
    events["stop_teleoperation"] = False
    try:
        while True:
            observation = robot.get_observation()
            action = teleop.get_action()
            robot.send_action(action)

            for obs_key, val in observation.items():
                if isinstance(val, float):
                    rr.log(f"observation/{obs_key}", rr.Scalars(val))
                elif isinstance(val, np.ndarray) and val.ndim in [2, 3]:
                    rr.log(f"observation/{obs_key}", rr.Image(val), static=False)
            
            for act_key, val in action.items():
                if isinstance(val, (float, int)):
                    rr.log(f"action/{act_key}", rr.Scalars(val))
    except KeyboardInterrupt:
        log_say("Teleoperation interrupted by user", True)
    finally:
        log_say("Teleoperation finished", True, blocking=True)

        robot.disconnect()
        teleop.disconnect()

        listener.stop()

    log_say("Exiting", True)

def record():
    pass

def main():
    parser = argparse.ArgumentParser(description="Robot box pickup script")
    parser.add_argument("--mode", type=str, default="teleop", choices=["teleop", "record"])
    args = parser.parse_args()

    if args.mode == "teleop":
        teleop()
    elif args.mode == "record":
        record()

if __name__ == "__main__":
    main()