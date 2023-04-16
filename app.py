from dbUtils import baseDb
from mqttpublishUtils import AquamateAdafruit
import time 
from googleFit import GoogleFit
from pushBulletUtils import PushBullet
from datetime import datetime

WEIGHT = 100
PIR = TEMPERATURE = 0

db = baseDb()
adafruit_obj = AquamateAdafruit()
gfit = GoogleFit()
pushbullet = PushBullet()


#initialise
adafruit_obj.publish_message(feed_name='weight', value = 100)
time.sleep(1)
adafruit_obj.publish_message(feed_name='temperature', value = 27)
time.sleep(1)
adafruit_obj.publish_message(feed_name='goal', value = 0)
time.sleep(1)
adafruit_obj.publish_message(feed_name='dynamic_goal', value = 0)

# db_initialise
db.update_data(collection='Config',filter={'PIR':True}, updated_data={'info': 'AquaMate', 'weight': 100, 'temperature': 27, 'drink': 0, 'time': {'hour': 0, 'min':0}})

print("Initialised.......")

while True:
    time.sleep(5)
    data = db.find_data(collection="Config")

    new_weight, new_PIR, new_temperature, prev_water_drank, schedule_time = data['weight'], data['PIR'], data['temperature'], data['drink'], data['time']
    time_now = datetime.now()
    if schedule_time:
        if schedule_time['hour'] == 0 and schedule_time['min'] == 0:
            db.update_data(collection='Config',filter={'PIR':True}, updated_data={'info': 'AquaMate'})
        elif schedule_time['hour'] <= time_now.hour and schedule_time['min']<time_now.minute:
            db.update_data(collection='Config',filter={'PIR':True}, updated_data={'info': 'Time to Drink Water'})
        else:
            db.update_data(collection='Config',filter={'PIR':True}, updated_data={'info': f"Next Schedule time: {schedule_time['hour']} hours and {schedule_time['min']} minutes"})
            
    if new_weight < WEIGHT:
        # drank water 
        # pushing notification 
        print("Drinking has been detected.................")
        db.update_data(collection='Config',filter={'PIR':True}, updated_data={'info': "Drinking Water......"})
        # percentage of water drank update
        percentage = WEIGHT - new_weight
        drank = 500 * (percentage/100)
        new_drink = prev_water_drank + drank 
        
        db.update_data(collection='Config',filter={'PIR':True}, updated_data={'drink': new_drink})
        adafruit_obj.publish_message(feed_name='goal', value = new_drink)
        
        gfit_data = gfit.predict_water_intake()
        adafruit_obj.publish_message(feed_name='dynamic_goal', value = str(gfit['prediction']))
        
        db.update_data(collection='Config',filter={'PIR':True}, updated_data={'time': {'hour': time_now.hour, "min": time_now.minute + 2}})
        
        message_template = f"\tAQUAMATE:\n\nWater Drank: {new_drink}\nGoal Set: {gfit_data['prediction']}\n\tACTIVITY MONITOR (Powered by - Google FIT):\nSTEPS: {gfit_data['steps']}\nCALORIES: {gfit_data['calories']} cals\nEXERCISE TIME: {gfit_data['exercise_mins']} mins\n\n NEXT DRINK SCHEDULED - {time_now.hour} hours and {time_now.minute + 2} minutes"
        pushbullet.notify(message_template)
        
        WEIGHT = new_weight
    
    if new_weight > WEIGHT:
        print("Refilling has been detected.................")
        WEIGHT = new_weight
    
    if TEMPERATURE != new_temperature:
        
        if new_temperature > 30:
            print("Heated Outcast has been detected, Please Drink more water..........")
            # Push Notification for heated outcast
            pushbullet.notify("Heated Outcast has been detected, Please Drink more water..........")
            
        TEMPERATURE = new_temperature
    
    print("SERVER UP...................")
    
    #try:
        #push to mqtt
    adafruit_obj.publish_message(feed_name='weight', value = WEIGHT)
    adafruit_obj.publish_message(feed_name='temperature', value = TEMPERATURE)
    # except Exception as e:
    #     print(str(e))
