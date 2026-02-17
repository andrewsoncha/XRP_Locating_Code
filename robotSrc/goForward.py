from XRPLib.defaults import *
from time import sleep

def drive():
    sleep(0.5)
    
    BASE_SPEED = 20
    STOP_DIST = 15
    Kp = 0.8
    # TARGET_COUNTS = 102
    
    imu.reset_yaw()
    
    print("Driving...")
    start_left_count = drivetrain.get_left_encoder_position()

    while True:
        left_count  = drivetrain.get_left_encoder_position()
        #if start_left_count == left_count:
        #    break
        if start_left_count is None:
            start_left_count = left_count
        right_count = drivetrain.get_right_encoder_position()
        
        left_rotations  = left_count / 288
        right_rotations = right_count / 288

        print(f"L Count: {left_count:.2f} | R Count: {right_count:.2f}")
        print(f"L Rotations: {left_rotations:.3f} | R Rotations: {right_rotations:.3f}")

        dist = rangefinder.distance()
        print(f"Range Distance: {dist:.1f} cm")
        
        if dist < STOP_DIST:
            drivetrain.stop()
            print(f"Wall detected < {STOP_DIST} cm. Stopped.")
            break
        
        current_yaw = imu.get_yaw()
        
        Y_set = 0.0
        error = Y_set - current_yaw
        
        correction = error * Kp
        
        left_speed = BASE_SPEED - correction
        right_speed = BASE_SPEED + correction
        
        drivetrain.set_speed(left_speed, right_speed)
        
        print(f"Yaw: {current_yaw:.2f} | Error: {error:.2f} | L: {left_speed:.2f} R: {right_speed:.2f}")
        
        sleep(0.05)
    
    drivetrain.stop()
    print("Drive complete.")

drive()
