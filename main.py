import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


def see_ports():     
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))


# ser = serial.Serial('/dev/tty.usbserial-120', 9600)  # Port adını ve baud hızını uygun şekilde değiştirin
# ser = serial.Serial('/dev/cu.usbserial-120', 9600)  # Port adını ve baud hızını uygun şekilde değiştirin



class pot_read:

    def __init__(self, port='/dev/tty.usbserial-120', baud_rate=9600):
        self.ser = serial.Serial(port, baud_rate)
        self.NUM_SLIDERS = 3 
        self.analogSliderValues = [0] * self.NUM_SLIDERS
        self.prevSliderValues = [0] * self.NUM_SLIDERS
        self.THRESHOLD = 1


    def see_ports(self):     
        for port, desc, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, desc, hwid))
    

    def scale_value(self, value, input_min, input_max, output_min, outpux_max):
        return int((value - input_min) * (outpux_max - output_min) / (input_max - input_min) + output_min) 
        
    def update_slider_values(self):
        # global analogSliderValues

        for i in range(self.NUM_SLIDERS):
            self.analogSliderValues[i] = int(self.ser.readline().decode('utf-8').rstrip().split('|')[i])

    
    # def any_slider_value_changed(self):
    #     # global analogSliderValues, prevSliderValues

    #     for i in range(self.NUM_SLIDERS):
    #         if self.analogSliderValues[i] != self.prevSliderValues[i]:
    #             self.prevSliderValues[i] = self.analogSliderValues[i]
    #             return True
    #     return False
    
    def any_slider_value_changed(self):
        for i in range(self.NUM_SLIDERS):
            if abs(self.analogSliderValues[i] - self.prevSliderValues[i]) > self.THRESHOLD:
                self.prevSliderValues[i] = self.analogSliderValues[i]
                return True
        return False



    def start(self):
        self.update_slider_values()

        if self.any_slider_value_changed():
            return tuple(self.analogSliderValues)
        else:
            return None
        

    def run(self):
        try:
            while True:
                values = self.start()
                if values:
                    x, y, z = values

                    x_scaled = self.scale_value(int(x),0, 1023, 0, 103)
                    y_scaled = self.scale_value(int(y),0, 1023, 0, 103)
                    z_scaled = self.scale_value(int(z),0, 1023, 0, 103)
                    
                    print(f"x: {x_scaled}, y: {y_scaled}, z: {z_scaled}")

        except KeyboardInterrupt:
            pass
        finally:
            self.ser.close()


            
if __name__ == '__main__': 
    startapp = pot_read()
  
    try:     
        startapp.run()
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        startapp.ser.close()
  

x = see_ports()
print(x)


# y = run()

