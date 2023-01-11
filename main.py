import cv2
import numpy as np
from windowcapture import WindowCapture
from eyeballs import Eyes
from time import time, sleep


windowcap = WindowCapture('Old School RuneScape')

compeyes = Eyes(None)

#load trained model
cascade_willows = cv2.CascadeClassifier('Y:\\opencv projects\\ScapeEyesML\\cascadeOutput\\cascade.xml')

clock = time()

while True:

    clock = time()
    # get an updated image of the game
    screenshot = windowcap.get_window()

    # do object detection
    rectangles = cascade_willows.detectMultiScale(screenshot)

    # draw the detection results onto the original image
    detection_image = compeyes.draw_rectangles(screenshot, rectangles)

    # display the images
    cv2.imshow('Matches', screenshot)

    # close window matches window or create postive/negative screenshot for training    
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    elif key == ord('f'):
        cv2.imwrite('ScapeEyesML\positiveInput\{}.jpg'.format(clock), screenshot)
    elif key == ord('d'):
        cv2.imwrite('ScapeEyesML\\negativeInput\{}.jpg'.format(clock), screenshot)

'''
make neg text file by running python in terminal and giving these commands
from cascadeutils import generate_negative_description_file
generate_negative_description_file()
exit()

generate positive text file by using 
Y:\\opencv\\build\\x64\\vc15\\bin\\opencv_annotation.exe --annotations=pos.txt --images=positive/
Press 'c' to confirm.
Or 'd' to undo the previous confirmation.
When done, click 'n' to move to the next image.
Press 'esc' to exit.
Will exit automatically when you've annotated all of the images

create pos.vec
Y:\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

train with:
Y:/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascadeOutput/ -vec pos.vec -bg neg.txt -w 50 -h 50 -numPos 98 -numNeg 1000 -numStages 8 -minHitRate 0.95 -precalcValBufSize 8192

*** w and h must match from vec file ***

-precalcValBufSize <precalculated_vals_buffer_size_in_Mb> : Size of buffer for precalculated feature values (in Mb). The more memory you assign the faster the training process 
however keep in mind that -precalcValBufSize and -precalcIdxBufSize combined should not exceed you available system memory.

-precalcIdxBufSize <precalculated_idxs_buffer_size_in_Mb> : Size of buffer for precalculated feature indices (in Mb). The more memory you assign the faster the training process however
 keep in mind that -precalcValBufSize and -precalcIdxBufSize combined should not exceed you available system memory.

-acceptanceRatioBreakValue <break_value> : This argument is used to determine how precise your model should keep learning and when to stop.
 A good guideline is to train not further than 10e-5, to ensure the model does not overtrain on your training data. By default this value is set to -1 to disable this feature.

source:
https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html
'''