from machine import Pin, PWM
from time import sleep
import dht


MOTOR_PIN = 16  # GPIO16 for MOSFET gate
dht_pin = machine.Pin(2)
motor_pwm = PWM(Pin(MOTOR_PIN))
motor_pwm.freq(1000)
dht_sensor = dht.DHT22(dht_pin)
duty_lv2 = 65536
duty_lv1 = 32768
duty_stop = 0
duty_step = 8191


# Duty cycle range is 0–65535 
dht_sensor.measure()
temperature_celsius = dht_sensor.temperature()
print("Temperature: {:.2f} °C".format(temperature_celsius))
        
if temperature_celsius > 30:
    for duty in range(0, duty_lv2, duty_step):
        "motor_pwm.duty_u16(duty)"
        sleep(0.5)
        print("Speed (duty):", duty)
    duty_current_new = duty
                
elif temperature_celsius < 30 and temperature_celsius > 20:
    for duty in range(0, duty_lv1, duty_step):
        "motor_pwm.duty_u16(duty)"
        sleep(0.5)
        print("Speed (duty):", duty)
    duty_current_new = duty    
            
else:
    "motor_pwm.duty_16(duty_stop)"
    duty_current_new = duty_stop
    print("Speed (duty):", duty_stop)
        
sleep(5)

while True:
    try:
        dht_sensor.measure()
        temperature_celsius = dht_sensor.temperature()
        print("Temperature: {:.2f} °C".format(temperature_celsius))
    
        if temperature_celsius > 30:
            for duty in range(duty_current_new, duty_lv2, duty_step):
                "motor_pwm.duty_u16(duty)"
                sleep(0.5)
                print("Speed (duty):", duty)
            duty_current_new = duty
                
        elif temperature_celsius < 30 and temperature_celsius > 20:
            for duty in range(duty_current_new, duty_lv1, duty_step):
                "motor_pwm.duty_u16(duty)"
                sleep(0.5)
                print("Speed (duty):", duty)
            duty_current_new = duty
            
        else:
            for duty in range(duty_current_new, duty_stop-1, duty_step):
                "motor_pwm.duty_16(duty)"
                print("Speed (duty):", duty)
            duty_current_new = duty
        
        
    except Exception as e:
        print("Error in measurements:", e)
        
    sleep(5)
    
    
"""# Ramp up speed
    for duty in range(0, 65536, 8192):  # 0 to 100% in steps
        motor_pwm.duty_u16(duty)
        print("Speed (duty):", duty)
        sleep(1)

    # Hold full speed
    sleep(2)

    # Ramp down speed
    for duty in range(65535, -1, -8192):
        motor_pwm.duty_u16(duty)
        print("Speed (duty):", duty)
        sleep(1)

    # Motor off
    motor_pwm.duty_u16(0)
    print("Motor OFF")
    sleep(2)"""
