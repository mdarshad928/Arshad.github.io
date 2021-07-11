#for temperature
import sys, os
import socket
import glob
import time, datetime
#endfor temperature

#for gps
import serial              
from time import sleep
import sys
import pynmea2
#endfor gps

#for pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

pnChannel = "raspi-tracker";

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-8ed44166-da9b-11eb-8c90-a639cde32e15"
pnconfig.publish_key = "pub-c-ea107b98-84ca-4d18-af2a-163e4c394105"
uuid: 1234
pnconfig.ssl = False

def test_connection():
    try:
        socket.create_connection(('google.com',80))
        return True
    except:
       return False
 
pubnub = PubNub(pnconfig)
T=1;
while (test_connection()==False):
    if T is 1:
        print("No Internet! Waiting for Internet Connection...")
        T =2;
pubnub.subscribe().channels(pnChannel).execute()

#for pubnub

#for temperature
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


#for gps
port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=0.5)
#endfor gps

count = 1
try:
    while True:
        def read_temp_raw():
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines
 
        def read_temp():
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
#                 time.sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f
        temp_c, temp_f = read_temp() #for temperature
        while True:
            byte_data = (str)(ser.readline())
            received_data = byte_data[2:-5] #read NMEA string received
    #print(received_data)
    #print(type(received_data))
            if received_data[0:6] == "$GPRMC":
                break
        
        newmsg=pynmea2.parse(received_data)
        lat=newmsg.latitude
        lng=newmsg.longitude
        time=str(newmsg.timestamp)+'UTC'
        m=1;
#         while (test_connection()==False):
#             if m is 1:
#                 print("No Internet! Waiting for Internet Connection...")
#                 m=2;
        envelope = pubnub.publish().channel(pnChannel).message({
        'lat':lat,
        'lng':lng,
        'temp_c':temp_c,
        'temp_f':temp_f,
        'time':time
        }).sync()
        if count is 1:
#                 count = count+1
            print('Running', lat, lng, temp_c, temp_f, time)
#             print(type(lat))
#             print("publish timetoken: %d" % envelope.result.timetoken)
#         except PubNubException as e:
#             handle_exception(e)
                    
#         else:
#             envelope = pubnub.publish().channel(pnChannel).message({
#             'temp_c':temp_c,
#             'temp_f':temp_f
#             }).sync()
#             print('Running',temp_c, temp_f)
#             print("publish timetoken: %d" % envelope.result.timetoken)
# #             gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
#             print(gps)
            
except KeyboardInterrupt:
    sys.exit(0)
