from pickle import NONE
import time
from datetime import datetime
import adafruit_dht
import board
import Adafruit_ADS1x15
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import mysql.connector
import math
import platform
from sds011 import*
import time
import gpsd


# MQ9 configurations
RLOAD = 10.0
RZERO = 88.33
PARB = 0.5494
PARA = 1.844

#MQ 135 configurations
RZERO_mq135 = 60
PARA_mq135 = 123.047
PARB_mq135 = 2.17

#particle configuration
sensor = SDS011("/dev/ttyUSB0", use_query_mode=True)
sensor.sleep(sleep=False)
time.sleep(10)  # Time to let the sensor warm up



# DHT22 and ADS1115 Initialization
devi = adafruit_dht.DHT22(board.D4)
adc = Adafruit_ADS1x15.ADS1115(address=0x48)
GAIN = 1

#GPS
gpsd.connect()

#Server
host ='104.194.104.247'
user = 'Admin'
password = 'I6xH#w92K'
database = 'Gas'

def insert_data(timestamp, T_f, humidity, ppm, ppm_mq135, pm25, pm10,latitude, longitude, altitude):
    try:
        print("TEST1")
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        currentdate = datetime.now()
        currentdate = currentdate.strftime('%Y-%m-%d-%H-%M-%S')
        HostName_Combo = platform.node() +' ' + current_run.strftime('%Y-%m-%d-%H-%M-%S')#currentdate.strftime('%Y-%m-%d-%H-%M-%S')
        print("TEST2")
        cursor = connection.cursor()
        print("TEST3")
        insert_query = (
            #"INSERT INTO tbl_Data (HostName_datetimeStart,Hostname,datetime_start,datetime_end,AirSensor1,AirSensor2,AirSensor3,AirSensor4,AirSensor5,AirSensor6, latitude, longitude) "
            "INSERT INTO tbl_Data (HostName_datetimeStart,Hostname,datetime,AirSensor1,AirSensor2,AirSensor3,AirSensor4,AirSensor5,AirSensor6,latitude,longitude,altitude) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        print("TEST4")
        cursor.execute(insert_query, (HostName_Combo,platform.node(),currentdate,T_f, humidity, ppm,ppm_mq135,pm25,pm10,latitude,longitude,altitude))
        print("TEST5")
        connection.commit()
        print("TEST6")
        cursor.close()
        connection.close()
        print("Data inserted successfully.")
       
    except mysql.connector.Error as error:
        print(f"Failed to insert into MySQL table {error}")

current_run = datetime.now()

def get_gps_position():
    try:
        # Get gps data
        packet = gpsd.get_current()

        # Check if the position is valid
        if packet.mode >= 2:
            # Report GPS data if available
            latitude = packet.lat
            longitude = packet.lon
            time = packet.get_time(local_time=True)
            altitude = packet.alt if packet.mode == 3 else 0
        else: 
            return 0, 0, 0
        

    except Exception as e:
        print(f"Error getting GPS data: {e}")
        return 0, 0, 0

while True:
    now = datetime.now()

   
    try:
        temperature = devi.temperature
        T_f = temperature * 1.8 + 32
        humidity = devi.humidity
       
        raw_value = adc.read_adc(0, gain=GAIN)
        resistance = (10000.0 * raw_value) / (65535.0 - raw_value)
        ppm = PARA * math.pow((resistance/RZERO), -PARB)
        
        raw_value_mq135 = adc.read_adc(1, gain=GAIN)
        resistance_mq135 = (10000.0 * raw_value_mq135) / (65535.0 - raw_value_mq135)
        ppm_mq135 = PARA_mq135 * math.pow((resistance_mq135/RZERO_mq135), -PARB_mq135)
        
        pm25, pm10 = sensor.query()
        
        #latitude, longitude, altitude = get_gps_position()
        # Get gps data
        packet = gpsd.get_current()

        # Check if the position is valid
        if packet.mode >= 2:
            # Report GPS data if available
            latitude = packet.lat
            longitude = packet.lon
            #time = packet.get_time(local_time=True)
            altitude = packet.alt if packet.mode == 3 else 0
        
        #print(f"raw value_mq135: {raw_value_mq135}, resistance of MQ 135: {resistance_mq135}")
        print(f"Timestamp: {now}, Temperature: {T_f}F  , Humidity: {humidity}%, CH4: {ppm}ppm, CO2: {ppm_mq135}ppm, PM2.5: {pm25}ug/m^3, PM10: {pm10}ug/m^3, Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
        insert_data(now, T_f, humidity, ppm, ppm_mq135, pm25, pm10,latitude, longitude, altitude)

       
    except RuntimeError as e:
        print("Bad measurement, retrying. {e}")
        

    time.sleep(5)
    
