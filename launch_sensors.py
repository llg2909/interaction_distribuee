from sensor import VirtualSensor


sensor1 = VirtualSensor('Hygrometer','Humidity',5,'%','Rangueil')
sensor2 = VirtualSensor('Thermometer','Heat',5,'C°','Rangueil')
sensor3 = VirtualSensor('Thermometer2','Heat',5,'C°','Rangueil')
sensor4 = VirtualSensor('Barometer','Air pressure',5,'mbar','Rangueil')

sensor1.start_threads()
sensor2.start_threads()
sensor3.start_threads()
sensor4.start_threads()


