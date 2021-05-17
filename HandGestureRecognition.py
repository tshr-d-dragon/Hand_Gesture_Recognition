
# Controls window, Mute-play-pause-stop-Screenshot

import cv2
import time
import vlc
import mediapipe as mp
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
color = ()
parser.add_argument("-p", "--path", default='cv2/Video.avi', 
                    required = False, type = str, help='Give path of video file')
args = parser.parse_args()
vid_path = ''
for i in list(args.path):
    vid_path += i


# For vlc instance
vlc_player = vlc.MediaPlayer()
media = vlc.Media(vid_path)
vlc_player.set_media(media)
# vlc_player.video_set_scale(0.3)
vlc_player.play()
time.sleep(5)


a = [0, 0, 0, 0, 0]
flag = True


mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands = 1, min_detection_confidence = 0.7, 
                      static_image_mode = False, min_tracking_confidence = 0.7)


def Distance(x1, y1, x2, y2):
    '''
    To calculate distance between 2 points
    '''
    
    return int(((y2-y1)**2+(x2-x1)**2)**0.5)


def handsFuncs(frame, draw = True):
    '''
    Returns the co-ordinates (x, y) for all fingers
    '''
    
    global a

    results = hands.process(frame)
    
    if results.multi_hand_landmarks:
        h, w, c = frame.shape       
        
        # For gesture recognition
        # Co-ordinates of Thumb finger:
        x2, x4 = results.multi_hand_landmarks[0].landmark[2].x*w, results.multi_hand_landmarks[0].landmark[4].x*w
        if x4 > x2:
            a[0] = 0
        elif x4 < x2:
            a[0] = 1    
        
        # Co-ordinates of Index finger:
        y6, y8 = results.multi_hand_landmarks[0].landmark[6].y*h, results.multi_hand_landmarks[0].landmark[8].y*h
        if y8 < y6:
            a[1] = 1
        elif y8 > y6:
            a[1] = 0
        
        # Co-ordinates of Middle finger:
        y10, y12 = results.multi_hand_landmarks[0].landmark[10].y*h, results.multi_hand_landmarks[0].landmark[12].y*h
        if y12 < y10:
            a[2] = 1
        elif y12 > y10:
            a[2] = 0
        
        # Co-ordinates of Ring finger:
        y14, y16 = results.multi_hand_landmarks[0].landmark[14].y*h, results.multi_hand_landmarks[0].landmark[16].y*h
        if y16 < y14:
            a[3] = 1
        elif y16 > y14:
            a[3] = 0
        
        # Co-ordinates of Pinky finger:    
        y18, y20 = results.multi_hand_landmarks[0].landmark[18].y*h, results.multi_hand_landmarks[0].landmark[20].y*h
        if y20 < y18:
            a[4] = 1
        elif y20 > y18:
            a[4] = 0
        
        # Co-ordinates of Thumb and Index finger:  
        y4, x8 = results.multi_hand_landmarks[0].landmark[4].y*h, results.multi_hand_landmarks[0].landmark[8].x*w
        distance = Distance(x4, y4, x8, y8)
        
        if draw:
            cv2.line(frame, (int(x4), int(y4)), (int(x8), int(y8)), (255, 0, 0), 3)
            cv2.putText(frame, 'Dist: '+str(distance), (1100, 650), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            for i in results.multi_hand_landmarks:    
                mpDraw.draw_landmarks(frame, i, mpHands.HAND_CONNECTIONS)
                
        return frame, int(x8), int(y8), distance
    
    else:
        return frame, 0, 0, 0   # all 0 terms represents x, y, distance
    
 
def VLC(x, y, dist, Nfingers, save_sc_path):
    '''
    To set the VLC player as per gestures
    '''
    
    global flag 
    
    if dist > 200:
        dist = 200
    elif dist < 40:
        dist = 40
        
    DistToPer = (dist - 40)/160
    if DistToPer < 0.2:
        DistToPer = 0.2
            
    if ((50 < x < 450) and (50 < y < 150)):
        flag = 0
    elif ((550 < x < 1250) and (50 < y < 150)):
        flag = 1
            
    if flag:
        if Nfingers == 3:
            vlc_player.set_pause(1)
        elif Nfingers == 4:
            vlc_player.play()
        elif Nfingers == 2:
            vlc_player.stop()
        elif Nfingers == 0:
            vlc_player.audio_set_mute(1)
        elif Nfingers == 1:
            vlc_player.video_take_snapshot(num = 0, psz_filepath = save_sc_path, i_width = 0, i_height = 0)

    elif not flag:    
        vlc_player.video_set_scale(DistToPer)
        
    else :  # Nfingers != 0
        vlc_player.audio_set_mute(0)
        
    return None
    
    
def DrawBoxes(frame):
    '''
    To draw diffrent req boxes
    '''
    
    cv2.rectangle(frame, (50, 50), (450, 150), (255, 0, 0), -1)
    cv2.putText(frame, 'ZoomIN/OUT', (70, 110), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)    
    cv2.rectangle(frame, (550, 50), (1250, 150), (0, 255, 0), -1)
    cv2.putText(frame, 'Play(4)/Pause(3)/Stop(2)/Mute(0)/SC(1)', (570, 110), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    return frame    


def main():
    
    global a
    
    t, count_frames = 0, 0

    video = cv2.VideoCapture(0) 
    video.set(3, 1280) # width
    video.set(4, 720)  # height
    
    # frame_width = int(video.get(3)) 
    # frame_height = int(video.get(4)) 
    # vid_fps = int(video.get(5)) 
    # code_of_codec = int(video.get(6))
    # No_of_frames = int(video.get(7))  
    # size = (frame_width, frame_height) 
    
    # result = cv2.VideoWriter('cv2/Video.avi',  
    #                          cv2.VideoWriter_fourcc(*'MJPG'), 
    #                          10, size) 
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	save_sc_path = f'Pictures/Saved Pictures/{dt_string}.jpg'

        frame, x, y, dist = handsFuncs(cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB), draw = False)
        
        frame = DrawBoxes(frame)
        
        # To set the VLC player as per gestures
        VLC(x, y, dist, sum(a), save_sc_path)
        
        s = time.time()
        fps = int(1/(s-t))
        t = s
        cv2.putText(frame, 'FPS: '+str(fps), (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        cv2.imshow('frame', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        count_frames += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            vlc_player.stop()
            # result.write(frame)
            break
        
    # result.release()
    video.release() 
    
    cv2.destroyAllWindows()
    print("Done processing video")
    
    return None


if __name__ == "__main__":
    main()


