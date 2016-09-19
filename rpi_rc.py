#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk


#Define BCM Raspberry Pi pins for use
P0 = 17
P1 = 27
P2 = 22
P3 = 23
P4 = 24

class Pwm_Pins:
    def __init__(self):
        from RPi import GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(P0,GPIO.OUT)
        GPIO.setup(P1,GPIO.OUT)
        GPIO.setup(P2,GPIO.OUT)
        GPIO.setup(P3,GPIO.OUT)
        GPIO.setup(P4,GPIO.OUT)

        self.freq = [50, 50, 50, 50, 50]
        self.dc = [7.1, 7.1, 4.6, 7.1, 7.1]

        self.pin = [ GPIO.PWM(P0,self.freq[0]) \
                    ,GPIO.PWM(P1,self.freq[1]) \
                    ,GPIO.PWM(P2,self.freq[2]) \
                    ,GPIO.PWM(P3,self.freq[3]) \
                    ,GPIO.PWM(P4,self.freq[4])]

        #self.pin0 = GPIO.PWM(P0,self.freq[0])
        #self.pin1 = GPIO.PWM(P1,self.freq[1])
        #self.pin2 = GPIO.PWM(P2,self.freq[2])
        #self.pin3 = GPIO.PWM(P3,self.freq[3])
        #self.pin4 = GPIO.PWM(P4,self.freq[4])


    def set_freq(self,pin,hz):
        self.freq[pin] = hz
        self.pin[pin].ChangeFrequency(self.freq[pin])

    def set_dc(self,pin,dc):
        self.dc[pin] = dc
        self.pin[pin].ChangeDutyCycle(self.dc[pin])

    def update_pin(self,pin):
        self.pin[pin].ChangeFrequency(self.freq[pin])
        self.pin[pin].ChangeDutyCycle(self.dc[pin])

    def start(self):
        self.pin[0].start(self.dc[0])
        self.pin[1].start(self.dc[1])
        self.pin[2].start(self.dc[2])
        self.pin[3].start(self.dc[3])
        self.pin[4].start(self.dc[4])

    def stop(self):
        from RPi import GPIO
        self.pin[0].stop()
        self.pin[1].stop()
        self.pin[2].stop()
        self.pin[3].stop()
        self.pin[4].stop()
        GPIO.cleanup()

    def __del__(self):
        self.stop()




class MainWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interfaz.glade")
        handlers = {
            "on_delete": self.exit_all
        }

        self.builder.connect_signals(handlers)

        self.roll_scale = self.builder.get_object("roll_scale")
        self.roll_adj = self.builder.get_object("roll_adj")
        self.pitch_scale = self.builder.get_object("pitch_scale")
        self.pitch_adj = self.builder.get_object("pitch_adj")
        self.throttle_scale = self.builder.get_object("throttle_scale")
        self.throttle_adj = self.builder.get_object("throttle_adj")
        self.yaw_scale = self.builder.get_object("yaw_scale")
        self.yaw_adj = self.builder.get_object("yaw_adj")
        self.aux_scale = self.builder.get_object("aux_scale")
        self.aux_adj = self.builder.get_object("aux_adj")

        self.roll_adj.connect("value_changed",self.print_values)
        self.pitch_adj.connect("value_changed",self.print_values)
        self.throttle_adj.connect("value_changed",self.print_values)
        self.yaw_adj.connect("value_changed",self.print_values)
        self.aux_adj.connect("value_changed",self.print_values)
        self.pwm = Pwm_Pins()
        self.pwm.start()

    def show(self):
        self.window = self.builder.get_object("main_window")
        self.window.show_all()
        Gtk.main()

    def print_values(self,widget):
        print "ROLL: " + str(self.roll_adj.get_value()) + " - " \
            +"PITCH: " + str(self.pitch_adj.get_value()) + " - " \
            + "THROTTLE: " + str(self.throttle_adj.get_value()) + " - " \
            + "YAW: " + str(self.yaw_adj.get_value()) + " - " \
            + "AUX: " + str(self.aux_adj.get_value())

        if widget == self.roll_adj:
            self.pwm.set_dc(0,float(self.roll_adj.get_value()))

        if widget == self.pitch_adj:
            self.pwm.set_dc(1,float(self.pitch_adj.get_value()))

        if widget == self.throttle_adj:
            self.pwm.set_dc(2,float(self.throttle_adj.get_value()))

        if widget == self.yaw_adj:
            self.pwm.set_dc(3,float(self.yaw_adj.get_value()))

        if widget == self.aux_adj:
            self.pwm.set_dc(4,float(self.aux_adj.get_value()))


    def exit_all(self,args,extra):
        Gtk.main_quit()
        self.pwm.stop()

if __name__ == "__main__":
    window = MainWindow()
    window.show()
