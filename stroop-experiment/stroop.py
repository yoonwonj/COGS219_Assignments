import time
import sys
import os
import random
import numpy as np
from psychopy import visual,event,core,gui
from functions import make_incongruent, generate_trials, get_runtime_vars, import_trials, write_responses

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

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
trial_types=['c','ic']

#get runtime variables
runtime_vars_order =  ['subj_code','seed','num_reps']
runtime_vars= get_runtime_vars({'subj_code':'stroop_101', 'seed':123, 'num_reps':25}, runtime_vars_order)
print(runtime_vars)

# generate trials
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],stimuli,trial_types) # this line added in "Part2-runtie-variable" commit

#initialize trial number
trial_num=1

# read in trial information
script_dir = os.path.dirname(os.path.abspath(__file__))
trial_path= os.path.join(script_dir,'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)
print(trial_list[:5])

# prepare response file
script_dir = os.path.dirname(os.path.abspath(__file__))
try:
    os.mkdir(os.path.join(script_dir,'data')) # file path fixed to match windows computer
    print('Creating data directory')
except FileExistsError:
    print('Data directory exists; proceeding to open file')

separator=','
    
f = open(os.path.join(script_dir,'data',runtime_vars['subj_code']+'_data.csv'),'w') # file path fixed to match windows computer

#write header
header = separator.join(["subj_code","seed","word", 'color','trial_type','orientation','trial_num','response','is_correct','rt']) # define header
f.write(header+'\n') # start writing the response

# new loop
for cur_trial in trial_list:
    #set variables from cur_trial
    cur_word=cur_trial['word']
    cur_color=cur_trial['color']
    cur_trial_type=cur_trial['trial_type']
    cur_orient=cur_trial['orientation']

    #set word_stim object
    word_stim.setText(cur_word)
    if cur_orient=="upside_down":
        word_stim.ori = 180  # Rotate text 180 degrees
    else:
        word_stim.ori = 0  # Keep normal orientation
    word_stim.setColor(cur_color)

    #draw placeholder, instruction, and fixation cross
    placeholder.draw()
    fixation_cross.draw() 
    win.flip()
    core.wait(.5) #let that state stay for .5 seconds

    #remove filxation cross and let that state stay removed for .5 seconds before the presentation of the stimuli
    placeholder.draw() 
    win.flip()
    core.wait(.5)

    #draw placeholder, instruction, and stimuli
    placeholder.draw()
    word_stim.draw() 
    win.flip()

    #after presentation of the stinui, start timing=reset the timer right away
    timer.reset() 

    #get response
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
                is_correct=0
                feedback_incorrect.draw() #incorrect feedback
                win.flip()
                core.wait(1)
            else: #if it is correct
                is_correct=1
            write_responses(f, runtime_vars['subj_code'], runtime_vars['seed'], cur_word, cur_color, cur_trial_type, cur_orient, trial_num, keypress[0], is_correct, cur_rt)
            RT.append(cur_rt) #append cur_rt to RT only when the key pressed is not 'q'
            print(RT)

    else: #if the key was not pressed within 2 sec
        cur_rt= np.nan #if it gets timeout, store cur_rt value as np.nan value (to prevent messing up the order of response time appended to RT)
        is_correct= "timeout" #record is_correct variable as "timeout" if the key was not pressed within 2 sec
        write_responses(f, runtime_vars['subj_code'], runtime_vars['seed'], cur_word, cur_color, cur_trial_type, cur_orient, trial_num, np.nan, is_correct, cur_rt)
        RT.append(cur_rt) #append nan value (for missing RT due to timeout)
        print(RT)
        feedback_slow.draw()
        win.flip()
        core.wait(1)
