# created a separate file for functions.

def make_incongruent(cur_word, stimuli):

    import random

    temp_stimuli=stimuli.copy()
    temp_stimuli.remove(cur_word)
    incongruent_color=random.choice(temp_stimuli) # randomly select incongruent key among non-answer keys

    return incongruent_color

def generate_trials(subj_code, seed, stimuli:list, trial_types:list, num_repetitions=25):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    seed: an integer specifying the random seed
    num_repetitions: integer specifying total times that combinations of trial type (congruent vs. incongruent) and orientation (upright vs. upside_down) should repeat (total number of trials = 4 * num_repetitions)
    '''
    import os
    import random

    # define general parameters and functions here
    separator=","

	# set seed
    random.seed(int(seed))

    # trial parameters
    # colors=colors
    # trial_types=trial_types
    orientations=["unrotated","upside_down"]
    num_repetitions= int(num_repetitions)
    
    # create a trials folder if it doesn't already exist\
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        os.mkdir(os.path.join(script_dir,'trials')) # file path fixed to match windows computer
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')
    
    f = open(os.path.join(script_dir,'trials',subj_code+'_trials.csv'),'w') # file path fixed to match windows computer

    #write header
    header = separator.join(["subj_code","seed","word", 'color','trial_type','orientation']) # define header
    f.write(header+'\n') # start writing the file
    
    # write code to loop through creating and adding trials to the file here
    trial_data=[]
    for i in range(num_repetitions):
        for cur_trial_type in trial_types:
            for cur_orient in orientations:
                cur_word= random.choice(stimuli)
                if cur_trial_type == 'c': #fixed error
                    cur_color= make_incongruent(cur_word, stimuli)
                else:
                    cur_color= cur_word
                trial_data.append([subj_code,seed,cur_word,cur_color,cur_trial_type,cur_orient])

    # randomly present the stimuli
    random.shuffle(trial_data)

    # write the trials information to a file
    for cur_trial in trial_data:
        f.write(separator.join(map(str,cur_trial))+'\n')

    #close the file
    f.close()

    #runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="stroop_experiment_assignment"):
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    from psychopy import core, gui
    core.wait(0.1) #added for my laptop compatibility (Windows)
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    core.wait(0.1) #added for my laptop compatibility (Windows)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

def import_trials (trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names) # make sure the number of column names = number of columns
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

def write_responses (f, subj_code, seed, cur_word, cur_color, cur_trial_type, cur_orient, trial_num, response, is_correct, cur_rt):
    # create a data folder if it doesn't already exist\

    separator=','
    
    cur_response= [subj_code,seed,cur_word,cur_color,cur_trial_type,cur_orient, trial_num, response, is_correct, cur_rt]

    f.write(separator.join(map(str,cur_response))+'\n')





