import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.MediaRecord import VideoRecord
from olympe.messages.ardrone3.MediaRecordState import VideoRecordStateChanged
from olympe.messages import gimbal
from olympe.messages.follow_me import Start, Stop, TargetTrajectory

import time

# Connect to the drone
drone = olympe.Drone("192.168.42.1")
drone.connect()

def takeoff():
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=10)).wait()

def land():
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=10)).wait()

def start_recording():
    drone(VideoRecord(start=True)).wait()

def stop_recording():
    drone(VideoRecord(stop=True)).wait()

def follow_target(duration):
    # Assuming the target's trajectory is provided. Replace with actual target tracking logic.
    drone(Start(
        mode="geographic",
        target_latitude=48.8795,
        target_longitude=2.3675,
        target_altitude=10.0,
        target_course=0.0,
        target_horizontal_accuracy=1.0,
        target_vertical_accuracy=1.0,
        target_course_accuracy=1.0,
    )).wait()

    time.sleep(duration)

    drone(Stop()).wait()

try:
    # Take off
    takeoff()

    # Start video recording
    start_recording()

    # Follow the target for x minutes (e.g., 2 minutes)
    follow_target(2 * 60)  # duration in seconds

    # Stop video recording
    stop_recording()

finally:
    # Land the drone
    land()

    # Disconnect the drone
    drone.disconnect()
