import KeyPressModule as kp
from djitellopy import Tello
from time import sleep
import cv2


kp.init()
t = Tello()
t.connect()
t.streamon()

print("Battery:", t.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 30

    if kp.getKey("a"): lr = -speed
    elif kp.getKey("d"): lr = speed

    if kp.getKey("w"): fb = speed
    elif kp.getKey("s"): fb = -speed

    if kp.getKey("o"): ud = speed
    elif kp.getKey("p"): ud = -speed

    if kp.getKey("k"): yv = -speed
    elif kp.getKey("l"): yv = speed

    if kp.getKey("q"):  t.land()
    if kp.getKey("e"):  t.takeoff()

    return [lr, fb, ud, yv]



while True:
    vals = getKeyboardInput()
    print(vals[0] , vals[1] , vals[2])
    t.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    frame = t.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("Tello", frame)

    cv2.waitKey(1)
    sleep(0.1)
