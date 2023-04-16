from dbUtils import baseDb
from mqttpublishUtils import AquamateAdafruit
import time 
from googleFit import GoogleFit

WEIGHT = PIR = TEMPERATURE = 0

db = baseDb()
adafruit_obj = AquamateAdafruit()
gfit = GoogleFit()

#initialise
adafruit_obj.publish_message(feed_name='weight', value = 100)
adafruit_obj.publish_message(feed_name='temperature', value = 27)
adafruit_obj.publish_message(feed_name='goal', value = 0)

while True:
    time.sleep(5)
    data = db.find_data(collection="Config")

    new_weight, new_PIR, new_temperature, prev_water_drank = data['weight'], data['PIR'], data['temperature'], data['drink']
    
    if new_weight < WEIGHT:
        # drank water 
        # pushing notification 
        print("Drinking has been detected.................")
        
        # percentage of water drank update
        percentage = WEIGHT - new_weight
        drank = 500 * (percentage/100)
        new_drink = prev_water_drank + drank 
        
        db.update_data(collection='Config',filter={'PIR':True}, updated_data={'drink': new_drink})
        adafruit_obj.publish_message(feed_name='goal', value = new_drink)
        
        WEIGHT = new_weight
    
    if new_weight > WEIGHT:
        print("Refilling has been detected.................")
        WEIGHT = new_weight
    
    if TEMPERATURE != new_temperature:
        
        if new_temperature > 30:
            print("Heated Outcast has been detected, Please Drink more water..........")
            # Push Notification for heated outcast
        TEMPERATURE = new_temperature
    
    print("SERVER UP...................")
    
    #push to mqtt
    adafruit_obj.publish_message(feed_name='weight', value = WEIGHT)
    adafruit_obj.publish_message(feed_name='temperature', value = TEMPERATURE)
        