#from psychopy import visual, event, core, gui 
#import os
#import glob

#runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="experiment_code_for_reference"):
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    from psychopy import core, gui 
    core.wait(0.5)
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    core.wait(0.5)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')