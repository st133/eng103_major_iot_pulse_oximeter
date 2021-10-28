import tkinter
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN)
import max30102
import hrcalc

led_pin = 14
GPIO.setup(led_pin, GPIO.OUT)

from twilio.rest import Client
account_sid= 'AC826d74f9dfd2ace624c7469d0648fcf7'
auth_token = '4e7278e77b6230f2a6003f3d0ffc2bcf'
client = Client(account_sid, auth_token)



print("[INFO] MAX30102 Channel & I2C Address.")
m = max30102.MAX30102()
hrR = 0
spL = 0


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.TitleLbl = tkinter.Label(window, text="PULSE OXYMETER",font=("Arial", 20, 'bold'), fg = "black",relief="raised",borderwidth = 2)
        self.TitleLbl.pack(anchor=tkinter.CENTER, expand=True)

        self.TitleLbl = tkinter.Label(window, text="ENG103-MAJOR IOT",font=("Arial", 12, 'bold'), fg = "dark orchid",relief="raised",borderwidth = 1)
        self.TitleLbl.pack(anchor=tkinter.CENTER, expand=True)
        
        self.PulseLbl = tkinter.Label(window, text="[Heart Rate    : ]",font=("Arial", 20), fg = "red",relief="ridge",borderwidth = 2)
        self.PulseLbl.pack(anchor=tkinter.CENTER, expand=True)

        self.SPO2Lbl = tkinter.Label(window, text="[Oxygen Saturation   : ]",font=("Arial", 20), fg ="blue",relief="ridge",borderwidth = 2)
        self.SPO2Lbl.pack(anchor=tkinter.CENTER, expand=True)
       
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 30
        self.update()

        self.window.mainloop()

 
    def update(self):
        red, ir = m.read_sequential()
        hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)
        if(hrb == True and hr != -999):
            hrR = int(hr)
            #print("Heart Rate : ",hr2)
            self.PulseLbl['text'] = "[Heart Rate    : "+str(hrR)+"bpm]"
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
            #print("SPO2 : ",sp2)
            self.SPO2Lbl['text'] = "[Oxygen Saturation   : "+str(spL)+"%]"
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
        self.window.after(self.delay, self.update)
        


# Create a window and pass it to the Application object
root = tkinter.Tk()
root.geometry("+{}+{}".format(250, 50))
App(root, "PULSE OXIMETER")
GPIO.cleanup
