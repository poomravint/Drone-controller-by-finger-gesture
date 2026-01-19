
from time import sleep
import cv2
import time
import HandTrackingModule as htm



wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)  # เปลี่ยนเป็น 0
cap.set(3, wCam)
cap.set(4, hCam)


pTime = 0
detector = htm.handDetector(detectionCon=0.75)

#? Finger gesture detect
def fingersUp(lmList):
    fingers = []

    # Thumb
    if lmList[4][1] < lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers index to pinky
    tips = [8, 12, 16, 20]
    for tip in tips:
        if lmList[tip][2] < lmList[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# For control by fingers
def finger_Controller(f, Lmlist):
    print("Fingers =", f)
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30

    x_tip = lmList[8][1]
    x_base = lmList[5][1]

    if f == [1, 1, 1, 1, 1]:
        print("Command: TAKEOFF")
        # t.takeoff()
    elif f == [0, 1, 1, 1, 0]:
        print("Command: LAND")
        #t.land()
    elif f == [1, 0, 0, 0, 0]:
        print("Command: FORWARD")
        fb = speed
    elif f == [1, 1, 0, 0, 0]:
        print("Command: BACKWARD")
        fb = -speed
    elif f == [0, 1, 0, 0, 0]:
        if x_tip > x_base + 30:
            print("Command: RIGHT") #นิ้วชี้เอียงไปทางขวา ตามหน้าจอ
            lr = speed
        elif x_tip < x_base - 30:
            print("Command: LEFT") #นิ้วชี้เอียงไปทางขวา ตามหน้าจอ
            lr = -speed
    elif f == [0, 0, 0, 0, 1]:
        print("Command: LEFT")
        lr = -speed
    elif f == [0, 0, 1, 1, 0]:
        print("Command: ROTATE LEFT")
        yv = -speed
    elif f == [0, 1, 1, 0, 0]:
        print("Command: ROTATE RIGHT")
        yv = speed
    elif f == [1, 1, 1, 0, 0]:
        print("Command: UP")
        ud = speed
    elif f == [0, 1, 1, 1, 1]:
        print("Command: DOWN")
        ud = -speed
    return [lr, fb, ud, yv]

while True:


    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        f = fingersUp(lmList)
        vals = finger_Controller(f, lmList)
        print(vals[0] , vals[1] , vals[2], vals[3])
        # t.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    if not success:
        print("Cannot access camera")
        break
    cv2.imshow("Image", img)

    cv2.waitKey(1)
    sleep(0.05)

cap.release()
cv2.destroyAllWindows()


