import time
import sys
import os
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])
fixation_cross = visual.TextStim(win, text="+", height=15, color="black", pos=[0,0]) #set fixation cross: set height as 15 and color as black (as indicated in the instruction)
while True:
    cur_stim = random.choice(stimuli) #set the current stimuli
    word_stim.setText(cur_stim)
    word_stim.setColor(cur_stim)
    placeholder.draw()
    instruction.draw()
    fixation_cross.draw() #draw placeholder, instruction, and fixation cross
    win.flip()
    core.wait(.5) #let them display for .5 seconds
    placeholder.draw()
    instruction.draw() #remove filxation cross
    win.flip()
    core.wait(.5) #and let that state stay removed for .5 sec before the presentation of the stimuli
    placeholder.draw()
    instruction.draw()
    word_stim.draw() #draw placeholder, instruction, and stiuli
    win.flip()
    core.wait(1.0) #let the stmulus displayed for 1 seconds
    placeholder.draw()
    instruction.draw()
    win.flip() #remove the stimuli
    core.wait(.15) #let that state stay for .15 sec

    if event.getKeys(['q']):
        win.close()
        core.quit()