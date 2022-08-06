import conf
from boltiot import Sms, Bolt
import matplotlib.pyplot as plt
import json, time
import numpy as np
from datetime import datetime
import statistics


minimum_limit = 0
maximum_limit = 30  
d=[]
Time=[]
tem=[]
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

for p in range(0,5): 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    try:
            
            sensor_value = int(data['value'])
            Temp=(100*sensor_value)/1024
            print("temp:",Temp)
            d.append(Temp)
            if minimum_limit<Temp<maximum_limit:
                mybolt.digitalWrite(1,'LOW')
                t1="{0}".format(datetime.now().strftime("%H:%M:%S"))
                Time.append(t1)
                tem.append(Temp)
            elif Temp>maximum_limit:
                mybolt.digitalWrite(1,'HIGH')
            
        #sending message for crossing limit due to damage
            if Temp < minimum_limit:
                print("Making request to Twilio to send a SMS")
                response = sms.send_sms("The Current temperature is " +str(Temp))
                print("Response received from Twilio is: " + str(response))
                print("Status of SMS at Twilio is :" + str(response.status))
                now=datetime.now()
                t1="{0}".format(datetime.now().strftime("%H:%M:%S"))
                Time.append(t1)
                tem.append(Temp)
                mybolt.digitalWrite(1,'LOW')
            elif Temp>maximum_limit:
                print("Current temperature:",Temp)
                print("Turning fan on")
                mybolt.digitalWrite(1,'HIGH')
                now=datetime.now()
                t1="{0}".format(datetime.now().strftime("%H:%M:%S"))
                Time.append(t1)
                tem.append(Temp)
            #sending message for opening door
            #z score outlier
            list(data).append(Temp(value))
            #print("data:",d)
            mean1=statistics.mean(d)
            #print("m:",mean1)
            std1= statistics.stdev(d)
            #print("s:",std1)
            threshold=3
            outlier=[]
            for i in d:
                z=(i-mean1)/(std1)
                #print("z:",z)
                if z> threshold or z<threshold:
                    outlier.append(i)
            if len(outlier)>=1:
                print("Making request to Twilio to send a SMS")
                response = sms.send_sms("SOMEONE HAS OPENED THE DOOR")
                print("Response received from Twilio is: " + str(response))
                print("Status of SMS at Twilio is :" + str(response.status))
                now=datetime.now()
                t1="{0}".format(datetime.now().strftime("%H:%M:%S"))
                Time.append(t1)
                tem.append(Temp)
            
    except Exception as e: 
            print ("Error occured: Below are the details")
            print (e)
    time.sleep(10)
ypoints=np.array(tem)
plt.plot_date(Time,ypoints)
plt.xlabel('time')
plt.ylabel('temperature')
plt.title("temperature monitor")
plt.show()

        
