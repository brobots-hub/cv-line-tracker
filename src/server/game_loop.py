import time
#from PIL import Image
#import numpy
from recordclass import recordclass
import requests

class Hardware1:
    def __init__(self):
        from gpiozero import PWMLED

        self.motor1_pin = PWMLED(6)
        self.servo_pin = PWMLED(13)
        
        try:
            from picamera import PiCamera
            self.camera = PiCamera()
        except Exception as e:
            print('Camera is disabled due to error:', e)

    """
    Current power on first motor
    """
    @property
    def motor1(self):
        return self.motor1_pin.value
    @motor1.setter
    def motor1(self, value):
        self.motor1_pin.value = value

    """
    Current PWM signal on servo
    """
    @property
    def servo(self):
        return self.hw.servo_pin.value
    @servo.setter
    def servo(self, value):
        self.servo_pin.value = value

    def release(self):
        if self.camera:
            self.camera.close()
        if self.motor1:
            self.motor1_pin.close()
        if self.servo:
            self.servo_pin.close()

    def capture_opencv():
        stream = BytesIO()
        self.camera.capture(stream, format='rgb')
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        image = Image.open(stream)
        return numpy.array(image.convert('RGB'))

class HardwareOverHTTP:
    def __init__(self, address):
        import requests 
        self.url = f'http://{address}'
        self._motor1_value = 0
        self._servo_value = 0
    """
    Current power on first motor
    """
    @property
    def motor1(self):
        return self._motor1_value
    @motor1.setter
    def motor1(self, value):
        requests.post(url=self.url+'/api/v1/motor', data={'power': value})
        self._motor1_value = value

    """
    Current PWM signal on servo
    """
    @property
    def servo(self):
        return self._servo_value
    @servo.setter
    def servo(self, value):
        requests.post(url=self.url+'/api/v1/servo', data={'angle': value})
        self._servo_value = value

    def release(self):
        requests.post(url=self.url+'/api/v1/motor', data={'power': 0})
        requests.post(url=self.url+'/api/v1/servo', data={'angle': 0})


class RobotState:
    """
    Current robot logic processing speed
    """
    FPS = 0

    """
    Current hardware configuration
    """
    hw = None

    """
    Currently executed program, can be changed by handlers
    """
    program = None

    current_time = None

    default_motor_power = 0.2
    max_motor_power = 0.5


def slowly_rotate(state, dt, events):
    if not hasattr(state, 'slowly_rotate'):
        state.slowly_rotate = recordclass('SlowlyRotate', 'start_time state servo_pwm motor_pwm')(0,0,0,0)
    st = state.slowly_rotate
    
    for event in events:
        if event == 'left':
            st.servo_pwm = 0.21
        elif event == 'right':
            st.servo_pwm = 0.08
        elif event == 'forward':
            st.motor_pwm = max(state.max_motor_power, st.motor_pwm + 0.1)
        elif event == 'backward':
            st.motor_pwm = 0
    st.motor_pwm = 0.2
    st.servo_pwm = 0.21
    #print(st.state, state.current_time - st.start_time)
    if st.state == 'move':
        #print(f'current time: {state.current_time}, start time: {st.start_time}')
        if state.current_time - st.start_time < 1:
            state.hw.motor1 = st.motor_pwm
            #print(f'move, motor={state.hw.motor1} servo={state.hw.servo}')
        else:
            state.motor1 = 0
            st.state = 'stop'
            st.start_time = state.current_time
            #print(f'stop {state.hw.motor1}')
    else:
        if state.current_time - st.start_time < 1:
            state.hw.motor1 = 0
            state.hw.servo = 0.125
            print(f'stopped {state.hw.servo}')
        else:
            st.state = 'move'
            st.start_time = state.current_time
            state.hw.servo = st.servo_pwm
            print(f'stopped {state.hw.servo}')

class GameLoop:
    handlers = []
    sleep_delay = 0.01

    state = None
    hw = None

    def __init__(self, hw=None):
        self.state = RobotState()
        if not hw:
            self.hw = Hardware1()
        else:
            self.hw = hw
        self.state.hw = self.hw

    def get_events(self):
        return []

    def main(self):

        last_time = time.time()
        fps_time = time.time()
        fps = 0
        try:
            while True:
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time
                if current_time - fps_time >= 1000:
                    self.state.FPS = fps
                    fps_time = current_time
                    fps = 0
                self.state.current_time = current_time

                events = self.get_events()
                for handler in self.handlers:
                    handler.update_loop(self.state, dt, events)

                time.sleep(self.sleep_delay)
                fps += 1
        finally:
            self.hw.release()

#game = GameLoop(HardwareOverHTTP('192.168.43.77:8080'))
game = GameLoop(HardwareOverHTTP('192.168.88.76:8080'))
#game.state.program = slowly_rotate
class h1:
    def update_loop(self, st, dt, evs):
        slowly_rotate(st, dt, evs)
game.handlers = [ (h1()) ]
game.main()
