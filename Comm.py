import serial
import time

if __name__ == '__main__':
    
    # Setup serial communication 
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    x = 0
    while True:
        # Send text over serial, the Arduino will look for this keyword and do an action in response
        x += 1
        
        if x == 1:
            time.sleep(2)
            ser.write(b"gate,close\n")
        elif x == 2:
            ser.write(b"pay,$10.50\n")
        elif x == 3:
            ser.write(b"pay,\n")
        elif x == 4:
            ser.write(b"gate,open\n")
        time.sleep(2)
        
        # If there is a serial message waiting
        if ser.in_waiting > 0:
            
            # Decode and write it out to console
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            
