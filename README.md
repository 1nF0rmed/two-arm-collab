# Bimanual Collaboration

This repo is to demonstrate bimanual collaboration using the SO-101 Lerobot arms.

It also includes a single example to pick_up objects on a single arm.

## Setup

### Install LeRobot

Clone LeRobot in a directory above
```bash
git clone https://github.com/huggingface/lerobot.git
```

Move into this repo and install LeRobot + deps like so
```bash
pip install -e ../lerobot/".[feetech,smolvla,aloha,pi0,hilserl]"
```

### Find your cameras

```bash
python -m lerobot.find_cameras opencv
```
