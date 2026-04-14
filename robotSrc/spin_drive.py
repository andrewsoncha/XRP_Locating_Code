from XRPLib.defaults import *
from time import sleep

def spin():
    BASE_SPEED = 5
   
    imu.reset_yaw()
   
    print("Spinning...")
   
    while True:
        rangeDist = rangefinder.distance()
        current_yaw = imu.get_yaw()
        
        print(f"Yaw: {current_yaw:.2f}, Range rangeDistance: {rangeDist:.1f} cm")
       
        if abs(current_yaw) >= 340:
            drivetrain.stop()
            print("Reached 360 degrees.")
            break
       
        drivetrain.set_effort(0.5, -0.5)
       
        sleep(0.05)
   
    drivetrain.stop()
    drivetrain.reset_encoder_position()
    print("Spin complete.")

def drive_distance(distance=1):
    sleep(0.5)
    
    rangefinder = Rangefinder.get_default_rangefinder()
    
    TARGET_SPEED = 70
    current_base_speed = 0
    ACCEL_RATE = 2
    STOP_DIST = 15
    Kp = 1.2
    
    Ki = 0.01   # Integral constant 
    Kd = 0.8    # Derivative constant
    INTEGRAL_CLAMP = 30  # Prevents integral windup
    
    MAX_SPEED = 30
    
    def clamp(val, min_val, max_val):
        return max(min_val, min(max_val, val))
    
    imu.reset_yaw()
    previous_error = 0
    integral_error = 0
    
    print("Driving...")
    
    start_left_count = drivetrain.get_left_encoder_position()
    while True:
        dist = rangefinder.distance()
        if dist < STOP_DIST:
            drivetrain.stop()
            print("Wall detected.")
            break
        
        if current_base_speed < TARGET_SPEED:
            current_base_speed += ACCEL_RATE
            current_base_speed = min(current_base_speed, TARGET_SPEED)
            
        left_count  = drivetrain.get_left_encoder_position()
        right_count = drivetrain.get_right_encoder_position()
        
        left_distance_ft  = left_count / (288 / 9.2)
        right_distance_ft = right_count / (288 / 9.2)
        # print(f"L Rotations: {left_distance_ft:.3f} | R Rotations: {right_distance_ft:.3f}")
        
        if (left_distance_ft + right_distance_ft) / 2 >= distance:
            drivetrain.stop()
            break
        
        current_yaw = imu.get_yaw()
        error = -current_yaw

        # Integral
        integral_error += error
        integral_error = clamp(integral_error, -INTEGRAL_CLAMP, INTEGRAL_CLAMP)

        # Derivative
        derivative = error - previous_error

        correction = Kp * error + Ki * integral_error + Kd * derivative
        
        left_speed = current_base_speed - correction
        right_speed = current_base_speed + correction
        
        left_speed = clamp(left_speed, -MAX_SPEED, MAX_SPEED)
        right_speed = clamp(right_speed, -MAX_SPEED, MAX_SPEED)
        
        drivetrain.set_speed(left_speed, right_speed)
        
        previous_error = error
        
        sleep(0.02)

    drivetrain.stop()
    drivetrain.reset_encoder_position()
    print("Drive complete.")

print("Press button to start")
board.wait_for_button()
spin()
sleep(1)
# drive_distance(1)
sleep(1)
spin()
