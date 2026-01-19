from djitellopy import Tello
from time import sleep

t = Tello()
t.connect()

print("Battery:", t.get_battery())

try:
    t.takeoff()
    t.send_rc_control(0, 10, 0, 0)
    sleep(2)
    t.send_rc_control(0, 0, 0, 0)
    t.land()

finally:
    # ถ้าโปรแกรม crash ก็ยังพยายามปิดการเชื่อมต่อให้เรียบร้อย
    t.end()