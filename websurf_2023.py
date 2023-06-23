###This experiment is created based on 
###This experiment was created by Python on Feb.23, 2023 by Serena J. Gu 
from websurf_library import *
import websurf_constants as c

def run():
    import re
    import os
    import csv
    import random as rand
    import numpy as np
    import pandas as pd
    import psychopy
    from functools import partial
    from psychopy import visual, event, core, data, logging, gui
    from psychopy.hardware.emulator import launchScan


    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    #####################Experiment Imformation####################
    psychopy.useVersion('2022.2.5')
    expName = 'WedSurf'  # from the Builder filename that created this script
    expInfo = {'participant': '', 'group': '', 'session': '', 'sync': '5', 'TR': 2.000, 'volumes': 3500}
    MR_settings = {'TR': expInfo['TR'], 'volumes': expInfo['volumes'], 'sync':expInfo['sync'], 'skip':0}
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName

    #########################Saving Data File Info#################

    save_filename = f"{_thisDir}/data/{expInfo['participant']}_{expInfo['date']}"
    log_File = logging.LogFile(save_filename+'.log', level=logging.DEBUG)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    #########################Experiment Start######################
    blockorder= f"{_thisDir}/blockorder.xlsx"               
    df = pd.read_excel(blockorder)

    win = visual.Window([1512, 982],fullscr=True, winType='pyglet',
        monitor="testMonitor", units="height", color="#808080", colorSpace='hex',
        blendMode="avg")
    
    win.mouseVisible = False

    ###Give instruction and two practice###########################
    chainInstructions(win, c.INSTA, c.INSTB, c.INSTC)
    showOffer(win, c.PRACLOGO, c.STAY, c.SKIP, c.INSTD%(12), keyList=['2'])
    newInstruction(win, c.INSTF)
    for k in range(5):
        correctkey = []
        random_number = rand.randint(1, 4)
        random_pos = (rand.uniform(-0.45, 0.45), rand.uniform(-0.45, 0.45))
        correctkey.append(str(random_number))
        costkey = showDelay(win, random_number, random_pos, keyList=correctkey)
    newInstruction(win, c.INSTG)
    showOffer(win, c.PRACLOGO, c.STAY, c.SKIP, c.INSTD%(5), keyList=['1'])
    showBar(win, c.PRACLOGO, c.QUIT, c.INSTD%(5), 5, keyList=['2', 'space'])
    chainInstructions(win, c.INSTH, c.INSTI, c.INSTJ)

    ###Save Data###################################################
    with open(f"{save_filename}.csv", 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=["SubID", 
            "group", "trial", "delay","onset of trial", "onset of offer", "offset of offer", 
            "cuelogo", "keypress", "decision", "rt decision", 
            "onset of clip", "offset of clip", "duration of clip", 
            "onset of rating", "offset of rating", "rating", "rt rating",
            "offset of trial", "onset of numbers", "travelcost", "cost_key",
            "offset of numbers"])
        writer.writeheader()
        ################################################################
        ###########REAL EXPERIMENT STARTS HERE##########################
        ################################################################
        n_trial, blocknum, vidnum = 0, 0, 0
        vidlist = list(range(1,63))
        rand.shuffle(vidlist)
        basetime = core.getTime()
        ended = False

        globalClock = core.Clock()
        vol = launchScan(win, MR_settings, globalClock=globalClock)
        duration = MR_settings['volumes'] * MR_settings['TR']

        #for i in range(250): #on average 100 - 200 trials
        for i in range(250): #on average 100 - 200 trials
            vidnum += 1
            starttime = core.getTime() - basetime
            time = core.getTime() - basetime
            breaklist = [-1, 0, 480.0, 960.0, 1440.0, 999999.9]
            if round(time) >= breaklist[blocknum +1]: 
                blocknum += 1
                newCross(win)

            for index, row in df.iterrows(): #every trial we loop through LAND>ART>CAT>ANIMAL
                n_trial += 1
                decision = "Skip"
                delay = rand.randint(3, 30)
                cue = row['Logo']
                onsetoffer = core.getTime() - basetime
                press = showOffer(win, cue, c.STAY, c.SKIP, c.INSTD%(delay))
                offsetoffer = core.getTime() - basetime

                onsetclip, offsetclip, offsetrating, lenofclip = [float('inf')] * 4
                event.getKeys(keyList=None)

                if press[0][0] == '1':
                    pressquit = showBar(win, cue, c.QUIT, c.INSTD%(delay), delay)
                    if pressquit != [] and pressquit[0] == ['2']:
                        decision = "Quit"

                if press[0][0] == '1' and pressquit == []:
                    decision = "Stay"
                    ratings = showVideo(win, cue, c.VIDPATH%(row['Order'],row['Order'], vidlist[vidnum-1]))
                    onsetclip = ratings[3] - basetime
                    offsetrating = core.getTime() - basetime
                    offsetclip = ratings[2] - basetime
                    lenofclip = offsetclip - onsetclip
                else:
                    ratings = None


                #move between trials with random numbers between 1 to 4
                travelcost = []
                rand_list = []
                onsetnumber = core.getTime() - basetime
                for j in range(5):
                    correctkey = []
                    random_number = rand.randint(1, 4)
                    rand_list.append(random_number)
                    random_pos = (rand.uniform(-0.45, 0.45), rand.uniform(-0.45, 0.45))
                    correctkey.append(str(random_number))
                    costkey = showDelay(win, random_number, random_pos, keyList=correctkey)
                    travelcost.append(int(costkey[0][0]))
                offsetnumber = core.getTime() - basetime
                offsettrial = core.getTime() - basetime

                csvrow = {"SubID": expInfo['participant'], "group": expInfo['group'],
                    "trial": n_trial, "delay": delay, "onset of trial": starttime,
                    "onset of offer":onsetoffer, "offset of offer":offsetoffer, 
                    "cuelogo": row['Order'], "keypress":"None" if press is None else press[0][0], 
                    "decision":decision, "rt decision":"None" if press is None else press[1],
                    "onset of clip":onsetclip, "offset of clip":offsetclip, "duration of clip":lenofclip, 
                    "onset of rating":offsetclip, "offset of rating":offsetrating, 
                    "rating":"None" if ratings is None else ratings[0][0], 
                    "rt rating":"None" if ratings is None else ratings[1],
                    "offset of trial": offsettrial, "onset of numbers":onsetnumber, 
                    "travelcost":rand_list, "cost_key": travelcost, "offset of numbers":offsetnumber
                }
                writer.writerow(csvrow)
                csvfile.flush()

                #make sure the task is 35 minutes
                quittime = core.getTime() - basetime
                if quittime >= 2100.0: 
                    ended = True
                    newEnd(win, c.INSTK)
                    break

            if ended == True:
                break
    #cleanup
    win.close()
    core.quit()