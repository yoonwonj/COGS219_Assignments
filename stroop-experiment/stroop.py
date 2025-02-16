import time
import sys
import os
import random
import numpy as np
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])
fixation_cross = visual.TextStim(win, text="+", height=15, color="black", pos=[0,0]) #set fixation cross: set height as 15 and color as black (as indicated in the instruction)
feedback_incorrect= visual.TextStim(win,text="Incorrect", height=20, color="black", pos=[0,0]) #this line was already added in "Part1-RT-correction2", and therefore did not show up on "Part1-feedback" commit.
feedback_slow= visual.TextStim(win,text="Too slow", height=20, color="black", pos=[0,0])

instruction.autoDraw = True

#list for storing RTs
RT=[]
timer = core.Clock() #add timer

def make_incongruent(cur_word, stimuli):
    temp_stimuli=stimuli.copy()
    temp_stimuli.remove(cur_word)
    incongruent_color=random.choice(temp_stimuli) # randomly select incongruent key among non-answer keys

    return incongruent_color

trial_type=['c','ic']

while True:
    cur_word = random.choice(stimuli) #set the current stiuli(word)
    trial=random.choice(trial_type)

    if trial =='c': #set the current stimuli(color)
        cur_color=cur_word
    else:
        cur_color=make_incongruent(cur_word,stimuli)

    word_stim.setText(cur_word)
    word_stim.setColor(cur_color)
    placeholder.draw()
    fixation_cross.draw() #draw placeholder, instruction, and fixation cross
    win.flip()
    core.wait(.5) #let that state stay for .5 seconds
    placeholder.draw() #remove filxation cross
    win.flip()
    core.wait(.5) #and let that state stay removed for .5 seconds before the presentation of the stimuli
    placeholder.draw()
    word_stim.draw() #draw placeholder, instruction, and stiuli
    win.flip()
    timer.reset() #start timing=reset the timer(right after we draw word_stim)
    keypress= event.waitKeys(keyList=['r','o','y','g','b','q'],maxWait=2)
    if keypress: #if key was pressed
        if keypress[0]=='q': #if the key pressed was q
            # do not store cur_rt to RT
            print(RT) # print to make sure the response time for pressing 'q' was not stored to the list
            win.close()
            core.quit()
        else: #if the key pressed was not q
            cur_rt= timer.getTime() #get response time (for button press)
            if keypress[0]!=cur_word[0]: #if the key pressed is incorrect
                feedback_incorrect.draw() #incorrect feedback
                win.flip()
                core.wait(1)
            else: #if it is correct
                pass
            RT.append(cur_rt) #append cur_rt to RT only when the key pressed is not 'q'
            print(RT)
    else: #if the key was not pressed
        cur_rt= np.nan #if it gets timeout, store cur_rt value as np.nan value (to prevent messing up the order of response time appended to RT)
    #print(keypress)
        RT.append(cur_rt) #append nan value (for missing RT due to timeout)
        print(RT)
        feedback_slow.draw()
        win.flip()
        core.wait(1)



