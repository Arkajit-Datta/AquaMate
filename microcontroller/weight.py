from machine import Pin, enable_irq, disable_irq, idle


class HX711:
    def __init__(self, dout, pd_sck, gain=128):

        self.pSCK = Pin(pd_sck, mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pSCK.value(False)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1

        self.time_constant = 0.1
        self.filtered = 0

        self.set_gain(gain);

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.read()
        self.filtered = self.read()
        print('Gain & initial value set')

    def is_ready(self):
        return self.pOUT() == 0

    def read(self):
        # wait for the device being ready
        while self.pOUT() == 1:
            idle()

        # shift in data, and gain & channel info
        result = 0
        for j in range(24 + self.GAIN):
            state = disable_irq()
            self.pSCK(True)
            self.pSCK(False)
            enable_irq(state)
            result = (result << 1) | self.pOUT()

        # shift back the extra bits
        result >>= self.GAIN

        # check sign
        if result > 0x7fffff:
            result -= 0x1000000

        return result

    def read_average(self, times=1000):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def read_lowpass(self):
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return self.filtered

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def set_time_constant(self, time_constant=None):
        if time_constant is None:
            return self.time_constant
        elif 0 < time_constant < 1.0:
            self.time_constant = time_constant

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)

if __name__ == "__main__":
    hx = HX711(5, 4)
    hx.tare()
    val = hx.read()
    print("read - ", val)
    val = hx.get_value()
    print(val)
#
# import machine
# import time
#
# # Define the HX711 pins
# dout_pin = machine.Pin(4, machine.Pin.IN)  # D2
# pd_sck_pin = machine.Pin(5, machine.Pin.OUT)  # D1
#
# # Define the calibration factor for your specific HX711 module
# calibration_factor = 12345
#
# # Define the number of readings to average
# num_readings = 10
#
# def read_weight():
#     # Wait for the HX711 to settle
#     pd_sck_pin.value(0)
#     time.sleep(1)
#
#     # Read the raw sensor value
#     raw_value = 0
#     for i in range(num_readings):
#         #raw_value += machine.ADC(dout_pin).read()
#     raw_value /= num_readings
#
#     # Calculate the weight using the calibration factor
#     weight = raw_value / calibration_factor
#     print(weight)
#     return weight
#
# # Example usage
while True:
    weight = read_weight()
    print("Weight:", weight, "g")
    time.sleep(8)
