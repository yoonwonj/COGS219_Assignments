import cv2
import numpy as np
from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os

###################################################################################
######## 1. create a window, contour the image, show it is a visualstim ###########
###################################################################################

window_size = [418/2, 1224/2]

#define window and mouse
win = visual.Window([50,100], color="white", units='pix', checkTiming=False, fullscr=True)

instruction = visual.TextStim(win,text=("Please indicate how \n the activity of your body changes when you feel.."), height=20, color="black", pos=[-350,100], autoDraw=True)
Target = visual.TextStim(win,text="Love", height=20, color="black", pos=[-350,0], autoDraw=True)
mouse = event.Mouse(win=win)

#create a blue circle (cursor)
#circle = visual.Circle(win,lineColor="black",fillColor="white",size=[300,300],autoDraw=True)

# use openCV to contour the image
script_dir = os.path.dirname(os.path.abspath(__file__))
body_contour_path= os.path.join(script_dir,"Final_project_images","dummyG.png")
body_contour_cv = cv2.imread(body_contour_path, cv2.IMREAD_GRAYSCALE) #grayscale the image for #threshold() and findContours() function

# Apply thresholding to get a binary image
#_, binary = cv2.threshold(body_contour_cv, 128, 255, cv2.THRESH_BINARY_INV)  # Invert so the outline is white
_,binary = cv2.threshold(body_contour_cv, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) ## Otsu's thresholding, Invert so the outline is white

### plotting the resulting image: manipulation check
#from matplotlib import pyplot as plt
#plt.imshow(binary,'gray')

#plt.show()

# Find contours (only the external one)
contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# the extracted contours have three hierarchies. 
# contours[1] is noise. two are relevant: one is outer body contour, the other one is inner body contour. inner one is more accurate.
#print(contours) 
cnt= contours[2]
#cnt = np.vstack((contours[0],contours[2]))
#print(cnt)


### start of ChatGPT generated & manually modified ###
# Convert contour points from pixel coordinates to PsychoPy coordinates
def convert_to_psychopy_coords(contour_points, img_shape, win_size):
    # img_shape = (x,y)
    # window_size = (x,y)
    win_w, win_h = win_size
    img_w, img_h = img_shape
    psychopy_coords = []
    
    for point in contour_points:
        px, py = point[0]  # OpenCV stores contours in [[[x, y]]]
        # Scale coordinates to fit PsychoPy's coordinate system
        #x= px*win_w -win_w/2
        #y= win_h/2 -py*win_h
        x = (px / img_w) * win_w - win_w / 2  # Normalize width
        y = (win_h - (py / img_h) * win_h) - (win_h / 2)  # Normalize height (invert y)
        psychopy_coords.append((x, y))
    
    return psychopy_coords

### end of ChatGPT generated & manually modified ###

# Convert to PsychoPy-friendly coordinates
window_size=tuple(window_size)
image_shape=(418,1224) #width,height
# print(contour[0:3])
contour_points = convert_to_psychopy_coords(cnt, image_shape, window_size)
# print(contour_points[0:3])
# print(contour_points)

# Load and display the background image (body contour)
body_contour = visual.ShapeStim(win, 
                                vertices= contour_points,
                                lineColor="black",
                                fillColor=None,
                                autoDraw=True,
                                pos=[0,0])
body_contour.draw()
win.flip()
core.wait(3)

##########################################################
######## 2. enable drawing and save the result ###########
##########################################################

### start of ChatGPT generated & manually modified code ###
# Track drawing inside the contour
# paint_circle_list = []
max_time = 60

# Convert contour to OpenCV contour format
cv_contour = np.array(cnt, dtype=np.int32)

def convert_to_cv_coords(point, win_size, image_shape):
    """ Convert PsychoPy coordinates to OpenCV pixel coordinates """
    win_w, win_h = win_size
    img_w, img_h = image_shape
    px = int((point[0] + win_w / 2) / win_w * img_w)
    py = int((win_h / 2 - point[1]) / win_h * img_h)
    return px, py

drawing_timer = core.Clock()
drawing_timer.reset()

while drawing_timer.getTime() <= max_time:
    mx, my = mouse.getPos()
    # Convert to OpenCV coords (because shapes with flexible edges is hard to check if the mouse is inside the shape using Psychopy built-in function)
    px, py = convert_to_cv_coords((mx, my), window_size, image_shape) 
    if cv2.pointPolygonTest(cv_contour, (px, py), False) >= 0:  # Check if the mouse is inside body
        if mouse.getPressed()[0]:  # If left mouse button is pressed
            paint_circle = visual.Circle(win, lineColor=None, fillColor="red", size=[10, 10], opacity=0.3, autoDraw=True)
            paint_circle.pos = (mx, my)
            #paint_circle_list.append(paint_circle)

    win.flip()
### end of ChatGPT generated & manually modified code ###

# print(paint_circle_list)

# Save the final drawing
win.getMovieFrame()
win.saveMovieFrames(os.path.join(script_dir,'data','drawing.png'))

win.close()
core.quit()

# to do: change the target word per trial (now it's fixed to one target word: Love)
# to do: save the drawing as vectors of pixel values instead of a screenshot
# to do: put 'erase' function
# to do: put participant info, let the file name saved according to the participant info
# to do : resolve mouse loading time (loads too late)
# to improve : make the touch be recorded more continuous (if I move the mouse fast, the painting will not be recorded as 'continuous' but rather a dotted line)