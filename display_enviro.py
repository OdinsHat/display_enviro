#!/usr/bin/python3
"""EnviroPhat and DisplayTron class to show various environment values.

This script when run will activate the Diplay-A-Tron with its
associated buttons which will enable it to show different
environment variables from the Envirophat itself and other attached
sensors. Such as MQ sensors and a CCS811 sensor which gives CO2 and TVOC
values.

It is possible to use the Display-A-Tron buttons to scroll between
different environment variables as well as effect the display light levels.
"""

import sys
import time
import math
from time import sleep
import busio
import envirophat
import board
import adafruit_ccs811
import dothat
from dothat import touch


class ZeroWEnvironment:
    """Environment display class for my ZeroW Pi with attached Pi hats

    Envirophat and DisplayTron attached to ZeroW board. This
    class has switching and other functions to show
    values from analog to envirophat sensors using various
    libraries.
    """

    def __init__(self,
                 busio,
                 envirophat,
                 dothat,
                 board,
                 adafruit_ccs811):
        self.unit = 'hPa'
        self.light = envirophat.light
        self.weather = envirophat.weather
        self.motion = envirophat.motion
        self.analog = envirophat.analog
        self.dothat.backlight = dothat.backlight
        self.lcd = dothat.lcd

        i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.ccs811 = adafruit_ccs811.CCS811(i2c_bus)
        self.views = ['temp_hum', 'gas', 'co2_voc']
        self.current_view = self.views[0]
        self.prepare_lcd()

        self.dothat.backlight.rgb(255, 255, 255)

    def change_view(self, direction):
        """Change the current view shown to the next
        or previous one shown
        """
        if direction is "left":
            if self.current_view != 0:
                self.current_view = self.current_view - 1
            else:
                self.current_view = 2
        if direction is "right":
            if self.current_view < 2:
                self.current_view = self.current_view + 1
            else:
                self.current_view = 0

    def show_view(self):
        """Show a different selection of data dependent on
        the button pressed and current position
        """
        if self.current_view is 'temp_hum':
            self.show_weather()
        if self.current_view is 'gas':
            self.show_gas()
        if self.current_view is 'co2_voc':
            self.show_environment()
        else:
            self.show_error()

    def show_error(self):
        """
        Very basic way os stating an error has occured
        to the user via the Display-A-Tron
        """
        self.prepare_lcd()
        self.lcd.write("Error in displaying data")

    def prepare_lcd(self):
        """
        Clear the LCD and set cursor position to o,o of screen
        in preperation for writing data to it.
        """
        self.lcd.clear()
        self.lcd.set_cursor_position(0, 0)

    def show_weather(self):
        """
        Using the Envirophat sensors display the
        temperature and pressure
        """
        self.prepare_lcd()
        self.lcd.write("%.2f C" % weather.temperature())
        self.lcd.set_cursor_position(0, 1)
        self.lcd.write("%.2f hPA" % weather.pressure(unit=self.unit))

    def show_gas(self):
        """
        Show analog gas readings for MQ135 and MQ 5
        """
        self.prepare_lcd()
        analog_values = self.analog.read_all()
        mq5 = analog_values[0]
        mq135 = analog_values[1]
        self.lcd.write("MQ5 = {:f}".format(mq5))
        self.lcd.set_cursor_position(0, 1)
        self.lcd.write("MQ135 = {:f}".format(mq135))

    def show_environment(self):
        """
        Show the environment data from CCS811 chip
        connetced via I2c
        """
        self.prepare_lcd()
        self.lcd.write("CO2: %1.0f PPM" % self.ccs811.eco2)
        self.lcd.set_cursor_position(0, 1)
        self.lcd.write("TVOC: {:f} PPM".format(self.ccs811.tvoc))
        self.lcd.set_cursor_position(0, 2)
        print("Temp: {:f} C" % self.ccs811.temperature)

    def show_light(self):
        """
        Show the light sensor readings from the Envirophat
        """
        rgb = self.light.rgb()
        self.prepare_lcd()
        self.lcd.write("Light Level: {:f}".format(self.light.light()))
        self.lcd.set_cursor_position(0, 2)
        self.lcd.write("RGB Values: {0}, {1}, {2}".format(rgb[0], rgb[1], rgb[2]))


def display_environment():
    """Display environment data on the Displaytron
    using the ZeroWEnvironment class.
    An infinite loop with a sleep to ensure
    display is refreshed every 1 second.

    Also a collection of methods are defined
    which activate the buttons of the Display-A-Tron.
    """
    while True:
        try:
            enviro = ZeroWEnvironment(busio,
                                      envirophat,
                                      dothat,
                                      board,
                                      adafruit_ccs811)

            @touch.on(touch.UP)
            def touch_up(chan, event):
                """
                When the UP button is pressed
                """
                dothat.backlight.rgb(255, 255, 255)

            @touch.on(touch.DOWN)
            def touch_down(chan, event):
                """
                When the UP button is pressed
                """
                dothat.backlight.off()

            @touch.on(touch.LEFT)
            def touch_left(chan, event):
                """
                When the LEFT button is pressed
                """
                enviro.change_view("left")
                enviro.show_view()

            @touch.on(touch.RIGHT)
            def touch_right(chan, event):
                """
                When the RIGHT button is pressed
                """
                enviro.change_view("right")
                enviro.show_view()

            @touch.on(touch.CANCEL)
            def touch_cancel(chan, event):
                """
                When the CANCEL button is pressed
                """
                x = 1
                dothat.backlight.sweep((x % 360) / 360.0)
                dothat.backlight.set_graph(abs(math.sin(x / 100.0)))

            @touch.on(touch.BUTTON)
            def touch_button(chan, event):
                """
                When the OTHER button is pressed
                """
                dothat.backlight.rgb(128, 128, 128)

            enviro.show_view()
            time.sleep(1000)

        except:
            e = sys.exc_info()[0]
            print("Error: {:s}".format(e))


if __name__ == '__main__':
    display_environment()