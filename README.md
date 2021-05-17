# Hand_Gesture_Recognition

### Hand Gesture Recognition and its application to control VLC Media Player using OpenCV

An OpenCV project that controls VLC Media Player by using the different hand gestures like:
1. Adjust Zoom In/Out of the video window using tip of the Index finger and Thumb.
2. Mute the video when no finger gesture (knuckle) is shown.
3. Take the Snapshot of the current frame and save it to preferred location when only one finger gesture is shown.
4. Stop the video when two finger gesture is shown.
5. Pause the video when three finger gesture is shown.
6. Play the video when four finger gesture is shown.

It uses Google's mediapipe library to detect the tip of the Index finger. For more information, please visit https://google.github.io/mediapipe/solutions/hands.

## To run the prject, follow below steps
1. Ensure that you are in the project home directory
2. Create anaconda environment
3. Activate environment
4. >pip install -r requirement.txt
5. >python HandGestureRecognition.py --path VIDEO_PATH

## Please feel free to connect for any suggestions or doubts!!!
