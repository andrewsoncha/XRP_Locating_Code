from XRPLib.defaults import *
from time import sleep
import math

robot_heading_deg = 0.0
robot_x = 0.0  
robot_y = 0.0

CM_PER_FOOT = 30.48

def spin():
    imu.reset_yaw()
    print("Spinning...")

    while True:
        rangeDist = rangefinder.distance()
        current_yaw = imu.get_yaw()
        print(f"Yaw: {current_yaw:.2f}, Range Distance: {rangeDist:.1f} cm")

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
    global robot_x, robot_y, robot_heading_deg

    distance_cm = distance_ft * CM_PER_FOOT
    print(f"Driving {distance_ft} ft ({distance_cm:.1f} cm)...")

    drivetrain.straight(distance_cm)

    heading_rad = math.radians(robot_heading_deg)
    robot_x += distance_cm * math.sin(heading_rad)
    robot_y += distance_cm * math.cos(heading_rad)

    print(f"Drive complete. Position: ({robot_x:.1f}, {robot_y:.1f}) cm")


def drive_to_point(target_x_ft, target_y_ft):
    global robot_heading_deg, robot_x, robot_y

    target_x_cm = target_x_ft * CM_PER_FOOT
    target_y_cm = target_y_ft * CM_PER_FOOT

    dx = target_x_cm - robot_x
    dy = target_y_cm - robot_y

    distance_to_target_cm = math.sqrt(dx**2 + dy**2)

    if distance_to_target_cm < 1.0:
        print("Already at target.")
        return

    target_heading = math.degrees(math.atan2(dx, dy))
    turn_angle = target_heading - robot_heading_deg
    turn_angle = (turn_angle + 180) % 360 - 180

    print(f"Current pos: ({robot_x/CM_PER_FOOT:.2f}, {robot_y/CM_PER_FOOT:.2f}) ft")
    print(f"Target: ({target_x_ft:.2f}, {target_y_ft:.2f}) ft")
    print(f"Distance: {distance_to_target_cm/CM_PER_FOOT:.2f} ft, Turning: {turn_angle:.1f} deg")

    drivetrain.turn(turn_angle)
    robot_heading_deg = target_heading

    drivetrain.straight(distance_to_target_cm)

    robot_x = target_x_cm
    robot_y = target_y_cm
    print("Arrived at target.")


print("Press button to start")
board.wait_for_button()

spin()
sleep(1)
drive_distance(1)
sleep(1)
spin()
drive_to_point(0, 0)
