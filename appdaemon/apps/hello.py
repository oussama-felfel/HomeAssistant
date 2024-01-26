import appdaemon.plugins.hass.hassapi as hass

#
# Hellow World App
#
# Args:
#

class HelloWorld(hass.Hass):

  def initialize(self):
    self.log("Hello from AppDaemon")
    self.log("You are now ready to run Apps!")

    self.set_state("sensor.u4test2", state="40", {"platform": "mqtt",\
    "name": "s202CO2",\
    "state_topic": "u4/302/co2",\
    "value_template": "{{ value_json.value }}",\
    "icon": "mdi:molecule-co2",\
    "unit_of_measurement": "ppm"})
    #self.set_state("sensor.testDaemon", "40",)
    self.log("Created sensor")
