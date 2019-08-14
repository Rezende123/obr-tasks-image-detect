import serial
 
PORT = "/dev/ttyUSB0"
velocity = 9600
#Configura a serial e a velocidade de transmissao
ser = serial.Serial(PORT, velocity)

def Write(value):
    print("Sending: " + str(value))
    ser.write(value)

def Read():
    response = ser.readline().decode('utf-8')
    response = int(response)
    
    print("Reading: " + str(response))

    return response