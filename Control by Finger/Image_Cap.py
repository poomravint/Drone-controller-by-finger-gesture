from djitellopy import Tello
import cv2

t = Tello()
t.connect()
print(t.get_battery())

t.streamon()

while True:
    frame = t.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow("Tello", frame)
    cv2.waitKey(1)
