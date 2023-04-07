from psychopy import visual, event, core
from psychopy.hardware import keyboard
from random import uniform

from threading import Thread

def newCross(win, pos=(0,0)):
    cross = visual.ShapeStim(
        win=win, name='fixationcross', vertices='cross',
        size=(0.045, 0.045), ori=0.0, pos=pos,
        lineWidth=1.0, colorSpace='rgb',  lineColor='black', fillColor='black',
        opacity=None, depth=0.0, interpolate=True)
    cross.draw()
    win.flip()
    #core.wait(45)
    core.wait(4)

def newText(win, text, pos=(0, 0), color='black', height=0.045):
    return visual.TextStim(win=win, 
        text=text, font='Arial', pos=pos, height=height, wrapWidth=None, ori=0.0, 
        color=color, colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)

def newKey(keyList=None, maxWait=float('inf')):
    #print(f"newKey(keyList={keyList},maxWait={maxWait})")
    key = None
    if keyList is None:
        key = event.waitKeys(maxWait=maxWait)
    else:
        if 'escape' not in keyList:
            keyList.append('escape')
        key = event.waitKeys(keyList=keyList,maxWait=maxWait)
    if key is not None and 'escape' in key:
        core.quit()
    return key

def newImage(win, image=None, zoom=0.7, pos=(-0.3, -0.35), size=None):
    image = visual.ImageStim(
        win=win, name='image', units='norm', image=image, mask=None,
        ori=0, pos=pos, size=size, color=[1,1,1], colorSpace='rgb', 
        opacity=1, flipHoriz=False, flipVert=False,
        texRes=512, interpolate=True, depth=0.0)
    sz = image.size
    image.setSize((sz[0] * zoom, sz[1] * zoom))
    return image

def newRatingscale(win, name, pos=(0, -0.5)):
    ratingscale = visual.RatingScale(win=win, pos=pos, textColor='black', 
        lineColor='black', marker='triangle', markerColor='blue', name=name, size=1.0, 
        low=1, high=4, labels=[''], scale='', disappear=False, respKeys=['1','2','3','4'], 
        acceptKeys=['return'], showValue=True)
    return ratingscale


def newInstruction(win, text, pos=(0,0), keyList=None):
    inst = newText(win, text, pos=pos)
    inst.draw()
    win.flip()
    newKey(keyList=keyList)

def timedKey(keyList=None, maxWait=4.0):
    remainder = maxWait
    clock = core.getTime()
    key = event.waitKeys(keyList=keyList, maxWait=remainder)
    pressTime = float('inf')
    if key is not None:
        pressTime = core.getTime() - clock
    else:
        return None
    remainder = maxWait - pressTime
    core.wait(remainder)
    return key, pressTime

def pressKey(keyList=None):
    clock = core.getTime()
    key = event.waitKeys(keyList=keyList)
    pressTime = float('inf')
    if key is not None:
        pressTime = core.getTime() - clock
    else:
        return None
    return key, pressTime

def showDelay(win, text, pos=(0,0), keyList=None):
    inst = newText(win, text, pos=pos, height= 0.07)
    inst.draw()
    win.flip()
    return pressKey(keyList=keyList)

def showImage(win, img_path, keyList=['1','2','3','4'], zoom =0.5, pos=(0, 0.3)):
    image = newImage(win, image=img_path, zoom=zoom, pos=pos)
    image.draw()
    win.flip()
    return pressKey(keyList=keyList)

class ProgressBar:
    def __init__(self, win, duration, pos=(0, -0.05), size=(0.6, 0.1), keyList=['2']):
        self.ended = False
        self.win = win
        self.keyList = keyList
        self.duration = duration
        self.pos = pos
        self.size = size
        self.prog_bar_outline = visual.Rect(win=self.win, pos=self.pos, size=self.size, lineColor='White', fillColor=None)
        self.prog_bar = visual.Rect(win=self.win, pos=self.pos, size=[0, self.size[1]], fillColor='White')
        self.clock = core.getTime()
        self.keys = []

    def getTime(self):
        return core.getTime() - self.clock

    def getKeys(self):
        keys = event.getKeys(keyList=self.keyList)
        if keys:
            self.keys = [keys, self.getTime()]

    def draw(self):
        self.prog_bar_outline.draw()
        self.prog_bar.size = [self.size[0] * self.getTime() / self.duration, self.size[1]]
        self.prog_bar.pos = [self.pos[0] + (self.prog_bar.size[0] - self.size[0]) / 2, self.pos[1]]
        self.prog_bar.draw()
        self.getKeys()
        if (self.keys and self.keys[0][0] == '2') or self.getTime() > self.duration:
            self.ended = True

def showOffer(win, cue, stay, skip, txt, keyList=['1','2']):
    img = newImage(win, image=cue, zoom=0.4, pos=(0, 0.65), size=(0.5, 0.8))
    countdown = newText(win, text=txt, pos=(0, 0.1))
    staybutton = newImage(win, image=stay, zoom=0.25, pos=(-0.3, -0.45))
    skipbutton = newImage(win, image=skip, zoom=0.25, pos=(0.3, -0.45))
    bar = visual.Rect(win=win, pos=(0, -0.05), size=(0.6, 0.1), lineColor='White', fillColor=None)
    img.draw()
    countdown.draw()
    bar.draw()
    staybutton.draw()
    skipbutton.draw()
    win.flip()
    return pressKey(keyList=keyList)

def showBar(win, cue, quit, txt, duration, keyList=['2']):
    #print(cue)
    img = newImage(win, image=cue, zoom=0.4, pos=(0, 0.65), size=(0.5, 0.8))
    quitbutton = newImage(win, image=quit, zoom=0.25, pos=(0.3, -0.45))
    countdown = newText(win, text=txt, pos=(0, 0.1))
    progress = ProgressBar(win, duration, keyList=keyList)
    while not progress.ended:
        img.draw()
        countdown.draw()
        quitbutton.draw()
        progress.draw()
        win.flip()
        if progress.keys: 
            break
    # while not progress.keys:
    #     progress.getKeys()
    return progress.keys

def newVideo(win, vid=None, pos=(0,0)):
    video = visual.MovieStim(
        win=win, units='',noAudio = False,
        filename=vid, ori=0, pos=(0,0), opacity=1,
        loop=False, anchor='center', size=(0.8, 0.45),
        depth=-5.0)
    return video


def showVideo(win, cue, vids, keyList=['1','2','3','4']):
    img = newImage(win, image=cue, zoom=0.4, pos=(0, 0.65), size=(0.5, 0.8))
    video = newVideo(win, vid=vids, pos=(0,0))
    rating = newRatingscale(win, vids, pos=(0, -0.5))
    rating.reset()

    def drawEverything(draw_rating=False):
        img.draw()
        video.draw()
        if draw_rating:
            rating.draw()
        win.flip()

    video.play()
    vidstart = core.getTime()
    while video.status != visual.FINISHED:
        drawEverything()
        event.getKeys(keyList=None)
    vidstop = core.getTime()
    while rating.getRating() is None:
        drawEverything(draw_rating=True)
    clock = core.getTime()
    while (core.getTime() - clock < 0.5):
        drawEverything(draw_rating=True)
    video.stop()
    rating.acceptResponse('key response')
    return [str(rating.getRating())], rating.getRT(), vidstop, vidstart

def chainInstructions(win, *instructions):
    for instruction in instructions:
        newInstruction(win, instruction)
