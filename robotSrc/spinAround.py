from XRPLib.defaults import *
from XRPLib.rangefinder import Rangefinder
from time import sleep

def drive():
    print("Press the button once to start.")
    board.wait_for_button()
    sleep(0.5)
    
    rangefinder = Rangefinder.get_default_rangefinder()
   
    BASE_SPEED = 30
    STOP_DIST = 10
    Kp = 0.8
   
    imu.reset_yaw()
   
    print("Driving...")
   
    while True:
        rangeDist = rangefinder.distance()
        print(f"Range rangeDistance: {rangeDist:.1f} cm")
       
        if rangeDist < STOP_DIST:
            drivetrain.stop()
            print(f"Wall detected < {STOP_DIST} cm. Stopped.")
            break
       
        current_yaw = imu.get_yaw()
       
        Y_set = 0.0
        error = Y_set - current_yaw
       
        correction = error * Kp
       
#        left_speed = BASE_SPEED - correction
#        right_speed = BASE_SPEED + correction
       
        left_speed = BASE_SPEED
        right_speed = -BASE_SPEED

        drivetrain.set_speed(left_speed, right_speed)
       
        print(f"Yaw: {current_yaw:.2f} | Error: {error:.2f} | L: {left_speed:.2f} R: {right_speed:.2f}")
       
        sleep(0.05)
   
    drivetrain.stop()
    print("Drive complete.")

drive()
