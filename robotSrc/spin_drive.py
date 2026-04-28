from XRPLib.defaults import *
from time import sleep
import math

robot_x = 0
robot_y = 0
CM_PER_FOOT = 30.48
WALL_THRESHOLD_CM = 5.0

def spin():
    global robot_x, robot_y
    imu.reset_yaw()
    print("Spinning...")
    while True:
        rangeDist = rangefinder.distance()
        current_yaw = imu.get_yaw()
        print(f"Yaw: {current_yaw:.2f}, Range Distance: {rangeDist:.1f} cm, Robot Position: ({robot_x},{robot_y})")
        if abs(current_yaw) >= 340:
            drivetrain.stop()
            print("Reached 360 degrees.")
            break
        drivetrain.set_effort(0.5, -0.5)
        sleep(0.05)
    drivetrain.stop()
    drivetrain.reset_encoder_position()
    print("Spin complete.")

def drive_distance(distance_ft=1):
    global robot_x, robot_y
    distance_cm = distance_ft * CM_PER_FOOT

    drivetrain.set_effort(0.5, 0.5)
    while True:
        rangeDist = rangefinder.distance()
        if rangeDist <= WALL_THRESHOLD_CM:
            drivetrain.stop()
            print("Wall detected! Stopping.")
            return True
        left_pos = drivetrain.get_left_encoder_position()
        right_pos = drivetrain.get_right_encoder_position()
        avg_cm = ((left_pos + right_pos) / 2)
        if avg_cm >= distance_cm:
            drivetrain.stop()
            robot_y += distance_ft
            print(f"Drive complete. Robot Position: ({robot_x},{robot_y})")
            return False
        sleep(0.05)

print("Press button to start")
board.wait_for_button()

while True:
    spin()
    sleep(0.5)
    wall_hit = drive_distance(1)
    if wall_hit:
        print("Robot stopped due to wall. Done.")
        break
    sleep(0.2)
