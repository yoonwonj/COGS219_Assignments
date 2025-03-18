import cv2
import numpy as np
from psychopy import visual, event, core # import the bits of PsychoPy we'll need for this walkthrough
import os
import random
from body_map_draw_help import get_runtime_vars
import json

###################################################################################
######## 1. create a window, contour the image, show it is a visualstim ###########
###################################################################################

"""
#get runtime variables
order =  ['subj_code','test_mode']
# runtime_vars= get_runtime_vars({'subj_code':'101', 'test_mode':'practice'}, order)
runtime_vars= get_runtime_vars({'subj_code':['101','102','103','104','105'], 'test_mode':['Choose','practice','real']}, order)
print(runtime_vars)

if runtime_vars is None:
    core.quit()
"""

#instead of getting runtime variables, just define this in the command line
sbjcode= input("Subject code:")
seed= input("Seed:")

#define window, mouse, instructions, and buttons
win = visual.Window(color="white", units='pix', checkTiming=False, fullscr=True) #fullscr=True
#window_size=list(win.size)
#window_size[0] = 418 * (window_size[0] / window_size[1])
window_size = [418/2, 1224/2]
# window_size = [418/1.2, 1224/1.2]

print(window_size)

instruction = visual.TextStim(win,text=("Please indicate where \n the activity of your body increases when you feel.."), height=20, color="black", pos=[-350,100], autoDraw=True)
mouse = event.Mouse(win=win)
reset_text= visual.TextStim(win,text=("Reset"), height=20, color="black", pos=[350,100], autoDraw=True)
reset_button = visual.Rect(win, width=100, height=50, lineColor="black", pos= [350,100], autoDraw=True)
submit_text= visual.TextStim(win,text=("Submit"), height=20, color="black", pos=[350,-100], autoDraw=True)
submit_button = visual.Rect(win, width=100, height=50, lineColor="black", pos= [350,-100], autoDraw=True)
warning_message = visual.TextStim(win,text=("Please draw your response before submitting"), height=15, color="red", pos=[300,0])
warning_message2 = visual.TextStim(win,text=("Please draw more before submitting"), height=15, color="red", pos=[300,0])

#define stimuli list
#seed=int(runtime_vars['subj_code'])
#word_list = ['Anger','Fear','Disgust']
word_list = ['Anger','Fear','Disgust','Happiness','Sadness','Surprise','Neutral','Anxiety','Love','Depression','Contempt','Pride','Shame','Jealousy']
random.seed(int(seed))
random.shuffle(word_list)

print(word_list)

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
#core.wait(0.5)

##########################################################
######## 2. enable drawing and save the result ###########
##########################################################

# Track drawing inside the contour
paint_circle_list = []
mouse_pos_list= []
max_time = 10

# Check if the JSON file already exists. If it does, load the existing data; if not, create an empty dictionary
json_data_dict = {}

# Convert contour to OpenCV contour format
cv_contour = np.array(cnt, dtype=np.int32)

def convert_to_cv_coords(point, win_size, image_shape):
    """ Convert PsychoPy coordinates to OpenCV pixel coordinates """
    win_w, win_h = win_size
    img_w, img_h = image_shape
    px = int((point[0] + win_w / 2) / win_w * img_w)
    py = int((win_h / 2 - point[1]) / win_h * img_h)
    return px, py

for word in word_list:
    drawing_timer = core.Clock()
    drawing_timer.reset()

    Target = visual.TextStim(win, text=word, height=20, color="black", pos=[-350,0], autoDraw=False)
    Target.draw()
    win.flip()

    #while drawing_timer.getTime() <= max_time:
    #'submit' button is not pressed
    while mouse.isPressedIn(submit_button)==False or drawing_timer.getTime() < 1 or len(paint_circle_list)<=30:

        Target.draw()
        mx, my = mouse.getPos()

        # Confining the drawing to the body
        # Convert to OpenCV coords (because shapes with flexible edges is hard to check if the mouse is inside the shape using Psychopy built-in function)
        px, py = convert_to_cv_coords((mx, my), window_size, image_shape) 
        if cv2.pointPolygonTest(cv_contour, (px, py), False) >= 0:  # Check if the mouse is inside body
            if mouse.getPressed()[0]:  # If left mouse button is pressed
                paint_circle = visual.Circle(win, lineColor=None, fillColor="red", size=[10, 10], opacity=0.3)
                #paint_circle.autoDraw=True
                paint_circle.pos = (mx, my) #set the position of the circle on the location of the mouse
                paint_circle_list.append(paint_circle)
                mouse_pos_list.append([px,py]) #here, the mouse position stored is in OpenCV coords
                win.flip()

        # Draw all stored circles
        for paint_circle_stim in paint_circle_list:
            paint_circle_stim.draw()

        # if 'reset' button is pressed
        if mouse.isPressedIn(reset_button):
            paint_circle_list.clear()
            win.flip()

        # if 'submit' button is pressed when nothing is drawn
        if mouse.isPressedIn(submit_button) and len(paint_circle_list)==0 and drawing_timer.getTime() > 1:
            warning_message.draw()
            win.flip()

        # if 'submit' button is pressed when little is drawn
        if mouse.isPressedIn(submit_button) and 0<len(paint_circle_list)<=30 and drawing_timer.getTime() > 1:
            warning_message2.draw()
            win.flip()

    # Save the final drawing and mouse position
    if mouse.isPressedIn(submit_button) and drawing_timer.getTime() > 1 and len(paint_circle_list)>30:
        #save the drawing
        win.getMovieFrame()
        win.saveMovieFrames(os.path.join(script_dir,'data',f'{sbjcode}_{word}_drawing.png'))
        
        # save the mouse position :
        json_data_dict[word]= {"mouse_positions": mouse_pos_list}

        # clear the drawing for the next stimuli
        paint_circle_list.clear()
        win.flip()

# Write the updated data back to the JSON file
json_file_path = os.path.join(script_dir, 'data', f'{sbjcode}_mouse_position.json')
with open(json_file_path, 'w') as json_file:
    json.dump(json_data_dict, json_file)

win.close()
core.quit()

