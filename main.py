import cv2
import numpy as np
import pyautogui
from windowcapture import WindowCapture
from eyeballs import Eyes
from time import time, sleep
from threading import Thread
from detection import objDetection
from bot import RSBot, BotState


windowcap = WindowCapture('Old School RuneScape')
detect = objDetection('Y:\\opencv projects\\ScapeEyesML\\cascadeOutput\\cascade.xml')
compeyes = Eyes(None)
bot = RSBot((windowcap.offset_x, windowcap.offset_y))

clock = time()

bot_in_action = False

windowcap.start()
detect.start()
bot.start()

while True:

    clock = time()
    if windowcap.screenshot is None:
        continue

    detect.update(windowcap.screenshot)

    # draw the detection results onto the original image
    detection_image = compeyes.draw_rectangles(windowcap.screenshot, detect.rectangles)

    # display the images
    cv2.imshow('Matches', windowcap.screenshot)

    

    # close window matches window or create postive/negative screenshot for training    
    key = cv2.waitKey(1)
    if key == ord('q'):
        windowcap.stop()
        detect.stop()
        bot.stop()
        cv2.destroyAllWindows()
        break
    elif key == ord('f'):
        cv2.imwrite('ScapeEyesML\positiveInput\{}.jpg'.format(clock), windowcap.screenshot)
    elif key == ord('d'):
        cv2.imwrite('ScapeEyesML\\negativeInput\{}.jpg'.format(clock), windowcap.screenshot)

'''
make neg text file by cd into directory with project andrunning python in terminal and giving these commands
from cascadeutils import generate_negative_description_file
generate_negative_description_file()
exit()

generate positive text file by using 
Y:\\opencv-3.4.11\\opencv\\build\\x64\\vc15\\bin\\opencv_annotation.exe --annotations=pos.txt --images=positiveInput/
Press 'c' to confirm.
Or 'd' to undo the previous confirmation.
When done, click 'n' to move to the next image.
Press 'esc' to exit.
Will exit automatically when you've annotated all of the images

create pos.vec
Y:\\opencv-3.4.11\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

train with:
Y:\\opencv-3.4.11\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe -data cascadeOutput/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 250 -numNeg 1000 -numStages 8 -minHitRate 0.95 -precalcValBufSize 8192

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