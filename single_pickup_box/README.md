# Pick Up Bot

A robotic box pickup script using the LeRobot framework with SO101 robot and teleoperation capabilities.

## Overview

This script provides teleoperation and recording functionality for a robotic arm to pick up boxes. It uses dual cameras (wrist and top-mounted) for visual feedback and supports real-time visualization through Rerun.

## Requirements

- LeRobot framework
- SO101 robot hardware (follower and leader devices)
- OpenCV-compatible cameras

## Environment Setup

Create a `.env` file with the following variables:

```env
ROBOT_ID=green
ROBOT_PORT=/dev/tty.usbmodem5A460815141
TELEOP_ID=red
TELEOP_PORT=/dev/tty.usbmodem5A460827091
WRIST_CAMERA_INDEX=3
TOP_CAMERA_INDEX=1
```

## Usage

### Teleoperation Mode
```bash
python pick_up_bot.py --mode teleop
```

### Recording Mode (In Development)
```bash
python pick_up_bot.py --mode record --resume false
```

For dataset recording, currently use the LeRobot CLI:
```bash
python -m lerobot.record \
--robot.type=so101_follower \
--robot.port=/dev/tty.usbmodem5A460815141 \
--robot.id=green \
--robot.cameras="{ wrist: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
--teleop.type=so101_leader \
--teleop.port=/dev/tty.usbmodem5A460827091 \
--teleop.id=red \
--display_data=true \
--dataset.repo_id={your_huggingface_username}/pick_up_and_drop_cube \
--dataset.num_episodes=5 \
--dataset.single_task="Pickup and drop cube" \
--resume=true
```

## Camera Configuration

- **Wrist Camera**: 640x480 @ 30fps
- **Top Camera**: 640x480 @ 30fps

## Controls

- Use Ctrl+C to stop teleoperation
- Real-time observations and actions are logged to Rerun for visualization

## Status

- ✅ Teleoperation: Fully functional
- 🚧 Recording: In development (use LeRobot CLI for now)
