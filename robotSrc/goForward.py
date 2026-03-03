from XRPLib.defaults import *
from time import sleep

def drive():
    sleep(0.5)
    
    TARGET_SPEED = 70
    current_base_speed = 0
    ACCEL_RATE = 3 # amount speed increases each loop
    STOP_DIST = 15
    Kp = 1.2
    Kd = 0.8 # derivative gain
    MAX_SPEED = 100 # motors never exceed allowed speed
    
    def clamp(val, min_val, max_val): # Add limits to motors
        return max(min_val, min(max_val, val))
    
    imu.reset_yaw()
    previous_error = 0 # stores last loop’s error
    
    print("Driving...")

    while True:
        dist = rangefinder.distance()
        if dist < STOP_DIST:
            drivetrain.stop()
            print("Wall detected. Stopped.")
            break
        
        if current_base_speed < TARGET_SPEED:
            current_base_speed += ACCEL_RATE # slowly accelerate
            current_base_speed = min(current_base_speed, TARGET_SPEED)
        
        current_yaw = imu.get_yaw()
        error = 0.0 - current_yaw
        
        derivative = error - previous_error # measures how fast the yaw error is changing
        
        correction = Kp * error + Kd * derivative # position correction
        
        left_speed = current_base_speed - correction
        right_speed = current_base_speed + correction
        
        left_speed = clamp(left_speed, -MAX_SPEED, MAX_SPEED) # ensure speeds stay within range
        right_speed = clamp(right_speed, -MAX_SPEED, MAX_SPEED)
        
        drivetrain.set_speed(left_speed, right_speed)
        
        previous_error = error # update stored error for derivative calculation
        
        sleep(0.02)

    drivetrain.stop()
    print("Drive complete.")

drive()
