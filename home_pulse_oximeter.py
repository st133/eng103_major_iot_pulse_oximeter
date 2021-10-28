import max30102
import hrcalc
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN)

led_pin = 14
GPIO.setup(led_pin, GPIO.OUT)

from twilio.rest import Client
account_sid= 'AC826d74f9dfd2ace624c7469d0648fcf7'
auth_token = '4e7278e77b6230f2a6003f3d0ffc2bcf'
client = Client(account_sid, auth_token)
m = max30102.MAX30102()

hrR = 0
spL = 0

while True:
    red, ir = m.read_sequential()
    
    hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

    print("hr detected:",hrb)
    print("sp detected:",spb)
    
    if(hrb == True and hr != -999):
        hrR = int(hr)
        print("Heart Rate : ",hrR)
        if (hrR < 60):
            GPIO.output(led_pin, True)
            time.sleep(10)
            GPIO.output(led_pin, False)
            message = client.messages \
                .create(
                    body = 'ENG103 <<Sushil Thapa>> Health Alert: BPM is' +str(hrR)+'bpm',
                    from_ = '+13012501839',
                    to = '+61425434777'
                )
        
            exit()
    if(spb == True and sp != -999):
        spL = int(sp)
        print("SPO2       : ",spL)
        if(spL < 88):
            GPIO.output(led_pin, True)
            time.sleep(10)
            GPIO.output(led_pin, False)
            message = client.messages \
                .create(
                    body = 'ENG103 <<Sushil Thapa>> Health Alert: BPM is' +str(hrR)+'bpm',
                    from_ = '+13012501839',
                    to = '+61425434777'
                )
        
            exit()
        
GPIO.cleanup
