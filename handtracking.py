import cv2
import mediapipe #make sure corret interpreter is selected
import math
import osascript

def angleCalc(p1,p2,p3):
    ang = math.degrees(math.atan2(p1[1]-p3[1], p1[0]-p3[0]) - math.atan2(p2[1]-p3[1], p2[0]-p3[0]))
    return ang + 360 if ang < 0 else ang

def distanceCalc(p1,p2):
    return math.dist(p1,p2)


DrawM = mediapipe.solutions.drawing_utils
HandsM = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')


with HandsM.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    while True:
        ret,frame = cap.read()

        f1 = cv2.resize(frame, (640,480))

        results = hands.process(cv2.cvtColor(f1, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:
            for hlm in results.multi_hand_landmarks:
                DrawM.draw_landmarks(f1, hlm, HandsM.HAND_CONNECTIONS)
        
            #   to find the thumb and Index Finger
                p1 = (0,0)
                p2 = (0,0)
                p3 = (0,0)
                z = 0
                for point in HandsM.HandLandmark:
                    
                    normalizedLandmark = hlm.landmark[point]
                    pixelCoordinatesLandmark= DrawM._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)
                    
                    if point == 8: # index
                        if pixelCoordinatesLandmark is None:
                            continue
                        p1 = (pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1])
                        #z = n[2]
                        #print(normalizedLandmark[2])
                        #print(point)
                        #print(pixelCoordinatesLandmark[0])
                        #print(normalizedLandmark)
                    
                    if point == 4: # thumb
                        if pixelCoordinatesLandmark is None:
                            continue
                        p2 = (pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1])
                        #p2 = point
                        #print(point)
                        #print(pixelCoordinatesLandmark)
                        #print(normalizedLandmark)

                    if point == 0: # wrist
                        if pixelCoordinatesLandmark is None:
                            continue
                        p3 = (pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1])
                        #p3 = point
                        #print(point)
                        #print(pixelCoordinatesLandmark)
                        #print(normalizedLandmark)    
                
                # using angle
                #print(angleCalc(p2,p1,p3))


                # using distance
                temp = distanceCalc(p1,p2)
                print(temp)
                
                if (temp > 100):
                    vol = "set volume output volume " + str(100)
                    osascript.osascript(vol)

                elif temp < 40:
                    vol = "set volume output volume " + str(0)
                    osascript.osascript(vol)
                else:
                    vol = "set volume output volume " + str(50)
                    osascript.osascript(vol)
                #print(z)

        cv2.imshow("Frame", f1)
        key = cv2.waitKey(1) & 0xFF
           
        #Below states that if the |q| is press on the keyboard it will stop the system
        if key == ord("q"):
            break