from machine import Pin, PWM, ADC
from time import sleep
import dht


MOTOR_PIN = 16  
DHT_PIN = 2     
LIGHT_SENSOR_PIN = 26

motor_pwm = PWM(Pin(MOTOR_PIN))
motor_pwm.freq(1000)



dht_sensor = dht.DHT22(Pin(DHT_PIN))
light_sensor = ADC(Pin(LIGHT_SENSOR_PIN))

duty_lv2 = 65536  # Full speed 
duty_lv1 = 32768  # Half speed
duty_stop = 0     # Stopped
duty_step = 8192  # Steps
duty_current = 0  # Current duty cycle

while True:
    try:
        try:
            raw_value = light_sensor.read_u16()
            print("Light level",  raw_value)
            dht_sensor.measure()
            temperature_celsius = dht_sensor.temperature()
            print("Temperature: {:.2f} °C".format(temperature_celsius))
        except Exception as e:
            print("Sensor error:", e)
            sleep(1)
            continue  # Skip the rest of the loop this time

        # Your logic continues as before
        if temperature_celsius > 28 and raw_value > 5000 :
            target_duty = duty_lv2  
        elif temperature_celsius > 28 and raw_value <= 5000 :
            target_duty = duty_lv1
        else:
            target_duty = duty_stop  

        if duty_current < target_duty: 
            for duty in range(duty_current, target_duty + 1, duty_step):
                motor_pwm.duty_u16(duty)  
                print("Speed (duty):", duty)
                sleep(0.1) 
            duty_current = target_duty
        
        elif duty_current > target_duty:
            for duty in range(duty_current, target_duty - 1, -duty_step):
                motor_pwm.duty_u16(duty)  
                print("Speed (duty):", duty)
                sleep(0.1)  
            duty_current = target_duty

        sleep(2)

    except KeyboardInterrupt:
        motor_pwm.duty_u16(0)
        print("Stopped by user.")
        break
