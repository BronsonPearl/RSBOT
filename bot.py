import cv2
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt

#OLD SHCOOL ENUM
class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    CUTTING = 3
    BACKTRACKING = 4 

class RSBot:
    #constants
    INIT_SECONDS = 6
    CUTTING_SECONDS = 10
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    IGNORE_RADIUS = 130

    #threading properties
    stopped = True
    lock = None

    #properties
    state = None
    targets = []
    screeshot = None
    timestamp = None
    movement_screenshot = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0

    click_history = []


    def __init__(self, window_offset):
        self.lock = Lock()
        #start bot in init mode
        self.window_offset = window_offset
        self.window_w = window_offset[0]
        self.window_h = window_offset[1]
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screeshot = screenshot
        self.lock.release()

    def click_next_target(self):
        targets = self.targets_ordered_by_distance(self.targets)

        target_i = 0
        found_tree = False
        while not found_tree and target_i < len(targets):
            # if we stopped our script, exit this loop
            if self.stopped:
                break

        target_pos = targets[target_i]
        screen_x, screen_y = self.get_screen_position(target_pos)
        
        # move the mouse
        pyautogui.moveTo(x=screen_x, y=screen_y)
        # short pause to let the mouse movement complete and allow
        # time for the tooltip to appear
        sleep(1.250)
        # confirm tooltip
        if self.confirm_tooltip(target_pos):
            found_tree = True
        pyautogui.click()
        # save this position to the click history
        self.click_history.append(target_pos)
        target_i += 1

        return found_tree

    def targets_ordered_by_distance(self, targets):
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        # print(my_pos)
        # print(targets)
        # for t in targets:
        #    print(pythagorean_distance(t))

        # ignore targets at are too close to our character (within 130 pixels) to avoid 
        # re-clicking a tree we just cut
        targets = [t for t in targets if pythagorean_distance(t) > self.IGNORE_RADIUS]

        return targets

    def click_backtrack(self):
        # pop the top item off the clicked points stack. this will be the click that
        # brought us to our current location.
        last_click = self.click_history.pop()
        # to undo this click, we must mirror it across the center point. so if our
        # character is at the middle of the screen at ex. (100, 100), and our last
        # click was at (120, 120), then to undo this we must now click at (80, 80).
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        mirrored_click_x = my_pos[0] - (last_click[0] - my_pos[0])
        mirrored_click_y = my_pos[1] - (last_click[1] - my_pos[1])
        # convert this screenshot position to a screen position
        screen_x, screen_y = self.get_screen_position((mirrored_click_x, mirrored_click_y))
        print('Backtracking to x:{} y:{}'.format(screen_x, screen_y))
        pyautogui.moveTo(x=screen_x, y=screen_y)
        # short pause to let the mouse movement complete
        sleep(0.500)
        pyautogui.click()

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the WindowCapture __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])
   
   
    def have_stopped_moving(self):
        #grab screenshot to compare to see if moving
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screeshot.copy()
            return False
        
        #compare old screenshot to new
        result = cv2.matchTemplate(self.screeshot, self.movement_screenshot, cv2.TM_CCOEFF_NORMED)
        similarity = result[0][0]

        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            return True

        self.movement_screenshot = self.screeshot.copy()
        return False

    def start(self):
        self.stopped = False
        bot_thread = Thread(target=self.run)
        bot_thread.start()
    
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                #do no action until startup is complete
                if time() > self.timestamp + self.INIT_SECONDS:
                    #start serching when wait period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
            
            elif self.state == BotState.SEARCHING:
                #check given click points and click them
                success = self.click_next_target()
                #if successful, switch state to moving
                #else backtrack or hold current state
                if success:
                    self.lock.acquire()
                    self.state = BotState.MOVING
                    self.lock.release()
                else:
                    pass
            
            elif self.state == BotState.MOVING:
                if not self.have_stopped_moving():
                    sleep(0.5)
                else:
                    self.lock.acquire()
                    self.timestampe = time()
                    self.state = BotState.CUTTING
                    self.lock.release()
            
            elif self.start == BotState.CUTTING:
                # see if we are done utting
                if time() > self.timestamp + self.CUTTING_SECONDS:
                    #return to searching state
                    self.lock.acquire()
                    self.start = BotState.SEARCHING
                    self.lock.release()


    def get_screen_position(self, position):
        return (position[0] + self.offset_x, position[1] + self.offset_y)