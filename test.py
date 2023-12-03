import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


def see_ports():     
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))


ser = serial.Serial('/dev/tty.usbserial-120', 9600)  # Port adını ve baud hızını uygun şekilde değiştirin
# ser = serial.Serial('/dev/cu.usbserial-120', 9600)  # Port adını ve baud hızını uygun şekilde değiştirin

# NUM_SLIDERS = 3 
# analogSliderValues = [0] * NUM_SLIDERS 
# prevSliderValues = [0] * NUM_SLIDERS


class pot_read:

    def __init__(self, port='/dev/tty.usbserial-120', baud_rate=9600):
        self.ser = serial.Serial(port, baud_rate)
        self.NUM_SLIDERS = 3 
        self.analogSliderValues = [0] * self.NUM_SLIDERS
        self.prevSliderValues = [0] * self.NUM_SLIDERS

    def see_ports(self):     
        for port, desc, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, desc, hwid))
    

    def scale_value(self, value, input_min, input_max, output_min, outpux_max):
        return int((value - input_min) * (outpux_max - output_min) / (input_max - input_min) + output_min) 
        
    def update_slider_values(self):
        # global analogSliderValues

        for i in range(self.NUM_SLIDERS):
            self.analogSliderValues[i] = int(ser.readline().decode('utf-8').rstrip().split('|')[i])

    
    def any_slider_value_changed(self):
        # global analogSliderValues, prevSliderValues

        for i in range(self.NUM_SLIDERS):
            if self.analogSliderValues[i] != self.prevSliderValues[i]:
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
                    print(f"x: {x}, y: {y}, z: {z}")

        except KeyboardInterrupt:
            pass
        finally:
            ser.close()


# def update_slider_values():
#     global analogSliderValues

#     for i in range(NUM_SLIDERS):
#         analogSliderValues[i] = int(ser.readline().decode('utf-8').rstrip().split('|')[i])


# def any_slider_value_changed():
#     global analogSliderValues, prevSliderValues
#     for i in range(NUM_SLIDERS):
#         if analogSliderValues[i] != prevSliderValues[i]:
#             prevSliderValues[i] = analogSliderValues[i]
#             return True
#     return False


# def start2():
#     try:
#         while True:
#             update_slider_values()

#             for i in range(NUM_SLIDERS):
#                 if analogSliderValues[i] != prevSliderValues[i]:
#                     values_str = ', '.join(map(str, analogSliderValues))
#                     print(f"{values_str}")

#     except KeyboardInterrupt:
#         ser.close()

# def start():
#     update_slider_values()

#     if any_slider_value_changed():
#         return tuple(analogSliderValues)
#     else:
#         return None

# def run():
#     try:
#         while True:
#             values = start()
#             if values:
#                 x, y, z = values
#                 print(f"x: {x}, y: {y}, z: {z}")

#     except KeyboardInterrupt:
#         pass
#     finally:
#         ser.close()



            
if __name__ == '__main__': 
    startapp = pot_read()
  
    try:     
        startapp.run()
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        startapp.ser.close()
  

# def update():
#     pass

# def check_change():
#     pass

# def start1():
#     try:
#         while True:
#             serial_data = ser.readline().decode('utf-8').rstrip()

#             values = serial_data.split('|')
#             # print(serial_data)
                
#             global first, second, third
#             first = scale_value(int(values[0]),0, 1023, 0, 103)
#             second = scale_value(int(values[1]), 0, 1023, 0, 103)
#             third = scale_value(int(values[2]), 0, 1023, 0, 103)  
#             #evrensel olabilmesi için potansiyometrenin aldığı maks değeri al ve potans_max - y = 100 denklemi ile y yi ekrana
#             #yazdır ve ses değerleri için kullan
#             #ya da kalibrasyon ayarı yap

#             print(first, second, third)
            



    # except KeyboardInterrupt:
    #     # Program kullanıcı tarafından kapatıldığında seriyi kapatın
    #     ser.close()


x = see_ports()
print(x)


# y = run()



