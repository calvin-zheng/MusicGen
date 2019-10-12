import pyaudio
import wave
import time

def playSongs(data):
    s = data.song
    notesDict = dict()
    notesDict = mapNotesToFile(notesDict,data)
    newStr = ''
    for i in range(len(s)):
        newStr += s[i]
        if(i+1<len(s)):
            if(s[i+1] != "-"):
                newStr += ","
    notesList = newStr.split(",")
    for i in range(len(notesList)):
        noteLetter = notesList[i][0]
        actualNote = notesList[i]
        if(actualNote != "."):
            noteLoc = notesDict[noteLetter]
            playNote(noteLoc, actualNote)
        else:
            time.sleep(0.5)

def mapNotesToFile(d,data):
    notes = ['a','b','c','d','e','f','g']
    fileLocationStr = "Notes/"
    if(data.clefChoice == data.trebleClef or data.clefChoice == ''):
        fileEnding = "4.wav"
    else: fileEnding = "3.wav"
    orgFileEnding = fileEnding
    for note in notes:
        if(note == 'c'): fileEnding = "4.wav"
        else: fileEnding = orgFileEnding
        d[note] = fileLocationStr + note[0] + fileEnding
    return d

def playNote(noteLoc,note):
        #determines if note is a half note or whole note
        holdAmt = len(note)
        quarterNoteSpeed = 0.5
        length = holdAmt*quarterNoteSpeed #referenced stackoverflow (link below)
        #code below is in documentation but I also referenced stackoveflow
        noteFile = wave.open(noteLoc, 'rb')
        py_audio = pyaudio.PyAudio()
        stream = py_audio.open(format=py_audio.get_format_from_width
                               (noteFile.getsampwidth()),
                               channels=noteFile.getnchannels(),
                               rate=noteFile.getframerate(),
                               output=True)

        #URL: https://stackoverflow.com/questions/18721780/
        #     play-a-part-of-a-wav-file-in-python
        #code directly from stackoverflow
        # write desired frames to audio buffer #comme nt from stack overflow
        n_frames = int(length * noteFile.getframerate())
        frames = noteFile.readframes(n_frames)
        stream.write(frames)

        # close and terminate everything properly #comment from stackoverflow

        noteFile.close()
        stream.close()
        py_audio.terminate()


###########################################
#obtained this from course website and the demo on advanced tkinter:
# original fileName was imagesDemo1.py
# view in canvas
# read from file
# with transparent pixels
# get size, resize (zoom and subsample)

# image resized, made transparent with:
# http://www.online-image-editor.com/


from tkinter import *
import random

class Measure(object):
    #x,y are the top left corner
    def __init__(self,x,y):
        self.x0 = x
        self.y0 = y
        self.width = 200
        self.height = 50
        self.defW = self.width
        self.defH = self.height
        self.x1 = self.x0 + self.width
        self.y1 = self.y0 + self.height
        self.nBeats = 4

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,canvas):
        x0,y0,x1,y1 = self.x0,self.y0,self.x1,self.y1
        deltaY = self.height/5
        margin = 1
        canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline="")
        canvas.create_rectangle(x0+1,y0+1,x1-1,y1-1,fill="white",outline="")
        lineY0 = y0
        for i in range(5):
            canvas.create_line(x0,lineY0,x1,lineY0,fill="black")
            lineY0 += deltaY

    def drawLines(self,canvas):
        x0,y0,x1,y1 = self.x0,self.y0,self.x1,self.y1
        lineY0 = y0
        deltaY = self.height/5
        for i in range(5):
            canvas.create_line(x0,lineY0,x1,lineY0,fill="black")
            lineY0 += deltaY

    def enlarge(self,amount):
        self.width *= amount
        self.height *= amount
        self.x1 = self.x0 + self.width
        self.y1 = self.y0 + self.height

    def shrink(self,amount):
        self.width /= amount
        self.height /= amount
        self.x1 = self.x0 - self.width
        self.y1 = self.y0 - self.height

    def returnToDefaults(self,amount):
        self.width = self.defW
        self.height = self.defH
        self.x1 = self.x0 + self.width
        self.y1 = self.y0 + self.height

    def move(self,data):
        self.x0 -= 1
        self.x1 -= 1

    def onTimerFired(self,data):
        self.move(data)

class Note(object):
    def __init__(self, x, noteLetter, measure, data,color = "black"):
        self.measureYCoord = 0
        self.x = x
        self.y = 0
        self.note = noteLetter
        self.mapNoteOnMeasure(measure,data)
        self.deltaOX = 15
        self.deltaOY = 10
        self.deltaLY = 45
        self.deltaLX = 0
        self.lY = self.y + self.deltaOY/2
        self.color = color
        self.amtMove = random.randint(1,5)
        self.beat = 1
        self.measure = measure

    def setColor(self,color):
        self.color = color

    def draw(self, canvas,data):
        if(self.note == '.'):
            drawRest(canvas,self.x,self.y,data.image)
        else:

            dOX = self.deltaOX
            dOY = self.deltaOY
            dLY = self.deltaLY
            dLX = self.deltaLX
            color = self.color
            x0,y0 = self.x,self.y
            x1,y1 = self.x + dOX, self.y + dOY
            noteLineY = self.lY
            if(data.clefChoice == data.trebleClef or data.clefChoice == ''):
                canvas.create_oval(x0,y0,x1,y1,fill=color,outline="")
                canvas.create_line(x1,noteLineY,x1+dLX,noteLineY-dLY,fill=color,
                                   width = dLX)
            else:
                 canvas.create_oval(x0,y0,x1,y1,fill=color,outline="")
                 canvas.create_line(x0,noteLineY,x0,noteLineY+dLY,fill=color,
                                    width = dLX)
            if(self.note == 'c'):
                canvas.create_line(x0 - 2, self.y + dOY/2, x1 + 2, self.y +
                                   dOY/2,fill = color)

    def mapNoteOnMeasure(self,measure,data):
        measureHeight = measure.getHeight()
        '''actually start by mapping A B G F and E'''
        noteSpacingDifference = measureHeight//10
        if(data.clefChoice == data.trebleClef or data.clefChoice == ''):
            if(self.note == 'a'):
                spacingIndex = measure.y1 - (3 * noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'b'):
                spacingIndex = measure.y1 - (4  * noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'f'):
                spacingIndex = measure.y1 - (noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'g'):
                spacingIndex = measure.y1 - (2  * noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'e'):
                spacingIndex = measure.y1 - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'd'):
                spacingIndex = measure.y1
                self.y = spacingIndex
            elif(self.note == 'c'):
                spacingIndex = measure.y1 + noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == '.'):
                spacingIndex = measure.y0 + measureHeight//2
                self.y = spacingIndex
        else:
            if(self.note == 'a'):
                spacingIndex = measure.y0 - (noteSpacingDifference)
                self.y = spacingIndex
            elif(self.note == 'b'):
                spacingIndex = measure.y0 - (noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'f'):
                spacingIndex = measure.y0 + (2*noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'g'):
                spacingIndex = measure.y0 + (noteSpacingDifference) \
                                - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'e'):
                spacingIndex = measure.y0 + (3*noteSpacingDifference) \
                               - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'd'):
                spacingIndex = measure.y0 + (4*noteSpacingDifference) \
                               - noteSpacingDifference
                self.y = spacingIndex
            elif(self.note == 'c'):
                 spacingIndex = measure.y0 - 3* noteSpacingDifference
                 self.y = spacingIndex
            elif(self.note == '.'):
                spacingIndex = measure.y0 + measureHeight//2
                self.y = spacingIndex


    def enlarge(self, amount):
        self.deltaOX *= amount
        self.deltaOY *= amount
        self.deltaLY *= amount
        self.deltaLX += amount//2
        self.lY = self.y + self.deltaOY/2

    def onTimerFired(self,data):
        self.move()

    def __str__(self):
        return self.note

    def move(self):
        self.x -= 1

class HalfNote(Note):
    def __init__(self, x, noteLetter, measure, color = "black"):
        super().__init__(x, noteLetter, measure, color)
        self.margin = 1
        self.beat = 2

    def draw(self,canvas,data):
        super().draw(canvas,data)
        m = self.margin
        x0,y0 = self.x,self.y
        x1,y1 = x0 + self.deltaOX, y0 +self.deltaOY
        canvas.create_oval(x0+m,y0+m,x1-m,y1-m,fill="white",outline="")

class DottedHalfNote(HalfNote):
    def __init__(self, x, noteLetter, measure, color = "black"):
        super().__init__(x, noteLetter, measure, color)
        self.beat = 3

    def draw(self,canvas,data):
        color = self.color
        super().draw(canvas,data)
        spacing = 3
        x0,y0 = self.x + self.deltaOX + spacing, self.lY
        x1,y1 = x0 + spacing, y0 - spacing
        canvas.create_oval(x0,y0,x1,y1,fill=color,outline="")

class WholeNote(Note):
    def __init__(self,x,noteLetter,measure,color="black"):
        super().__init__(x,noteLetter,measure,color)
        self.beat = 4

    def draw(self,canvas,data):
        x0 = self.x
        y0 = self.y
        dOX = self.deltaOX
        dOY = self.deltaOY
        canvas.create_oval(x0,y0,x0+dOX,y0+dOY, fill = self.color)
        canvas.create_oval(x0+2,y0+1,x0-2+dOX,y0-1+dOY, fill = "white")

def buildAllMeasures(data):
    margin = 20
    nLines = data.height//100
    y0 = margin
    for line in range(nLines):
        if(y0 >= data.height or y0 + 100 >= data.height): break
        data.measureList += buildMeasureLine(data,3,y0)
        y0 += 100

def buildMeasureLine(data,x0,y0,counter=5):
    tempX = x0
    measureLine = []
    for i in range(counter):
        measureLine.append(Measure(tempX,y0))
        tempX += measureLine[0].getWidth()
    return measureLine

def drawAllMeasures(data,canvas):
    for measure in data.measureList:
        measure.draw(canvas)

def displayText(data,canvas):
    canvas.create_text(data.width//2,data.height//2 - 20,anchor = 'n',
                       text = data.song)

def displayTextScore(data,canvas):
    canvas.create_image(data.width//2,data.height//2 - 15,
                        image = data.youhavetypedsmall)
    canvas.create_text(data.width//2,data.height//2 - 10,anchor = 'n',
                       text = data.song)

def obtainNotesFromUI(data,event):
    notes = {'a','b','c','d','e','f','g','period','minus'}
    if(event.keysym in notes):
        if(event.keysym != "period" and event.keysym != "minus"):
            data.song += event.keysym
            data.currNote = event.keysym
        elif(event.keysym == "minus"):
            data.song += "-"
        else:
            data.song += "."
            data.currNote = "."

def drawUITypeWindow(canvas,data):
    w,h = data.width, data.height
    radius = 20
    xRadius = 400
    cx,cy = w/2,h/2
    canvas.create_image(cx,cy-radius*6,image = data.titleImage)
    data.titlePos = cx,cy-radius*6
    canvas.create_image(cx,cy-radius*4,image = data.beats)
    data.beatsPos = cx,cy-radius*3
    canvas.create_image(cx,cy-radius*2,image = data.youHaveTyped)
    canvas.create_rectangle(cx-xRadius,cy-radius,cx+xRadius,cy,fill="white")
    displayText(data,canvas)
    canvas.create_image(cx,cy+radius*3,image=data.chooseClef)
    xRadius = 50
    canvas.create_image(cx-xRadius,cy+radius*5,image=data.bassChoice)
    data.bcPos = (cx-xRadius,cy+radius*5)
    canvas.create_image(cx+xRadius,cy+radius*5,image=data.trebleChoice)
    data.tcPos = (cx+xRadius,cy+radius*5)
    for measure in data.startUpMeasures:
        measure.draw(canvas)
        measure.drawLines(canvas)
    for note in data.startUpNotesList:
        note.draw(canvas,data)
    drawMainMenuButton(data,canvas)


def drawMainMenuButton(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(w/8, 7*h/8, image = data.mainmenu)
    data.mmPos = w/8, 7*h/8


def drawRest(canvas, x , y , image):
    canvas.create_image(x,y,image = image)

def drawAllNotes(data,canvas):
    for note in data.noteList:
        note.draw(canvas,data)

def drawAnimationNotes(data,canvas):
    for note in data.animationNoteList:
        note.draw(canvas,data)

def drawAnimationClef(data,canvas):
    if(data.clefChoice == data.trebleClef):
        drawTrebleClef(data, canvas, data.animationMeasureList[0])
    if(data.clefChoice == data.bassClef):
        drawBassClef(data, canvas, data.animationMeasureList[0])

def drawScoreClef(data,canvas):
    if(data.clefChoice == data.trebleClef):
        drawTrebleClef(data, canvas, data.measureList[0])
    if(data.clefChoice == data.bassClef):
        drawBassClef(data, canvas, data.measureList[0])

def drawAnimationMeasures(data,canvas):
    for measure in data.animationMeasureList:
        measure.draw(canvas)

####################################
# customize these functions
####################################

def redrawAll(canvas, data):
    if(data.window == 1):
        drawStartUpLogo(data,canvas)
        drawStartUpOptions(data,canvas)
    if(data.window == 2):
        if(data.changeScreen and not data.animateSong):
            drawAllMeasures(data,canvas)
            drawAllNotes(data,canvas)
            displayTextScore(data,canvas)
            drawMainMenuButton(data,canvas)
            drawAnimateButton(data,canvas)
            drawScoreClef(data,canvas)
            drawPlayButton(data,canvas)
        elif(not data.animateSong):
            drawUITypeWindow(canvas,data)
            drawCreateYour(data,canvas)
    if(data.animateSong):
        drawAnimationMeasures(data,canvas)
        drawAnimationNotes(data,canvas)
        drawMainMenuButton(data,canvas)
        drawAnimationClef(data,canvas)
        drawPlayButton(data,canvas)
        drawBackButton(data,canvas)
        drawTitle(data,canvas)
    if(data.window == 3):
        drawHelpScreen(canvas,data)
    if(data.window == 4):
        drawBeatsSelectionWindow(data,canvas)
    if(data.window == 5):
        drawTitleWindow(data,canvas)

def drawPlayButton(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(7*w/8, 7*h/8, image = data.play)
    data.pPos = 7*w/8, 7*h/8

def drawAnimateButton(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(w/2, 7*h/8, image = data.animateImage)
    data.animatePos = w/2, 7*h/8

def drawHelpScreen(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="white",outline='')
    w,h = data.width,data.height
    canvas.create_image(w/2, h/8, image=data.helpScreen)
    canvas.create_image(w/2 + 1, h/8 + 1, image=data.helpScreen)
    canvas.create_image(w/2, h/4, image= data.helpScreen1)
    font = "Monaco 12"
    text = 'Return to the Main Menu and click on the option entitled ' + \
           '"Create Your Music Score"'
    canvas.create_text(w/2, h/4 + 30, text = text, font = font)
    text = "You will see the option to modify the beats per measure. " + \
           "Click on that if you"
    canvas.create_text(w/2, h/4 + 45, text = text, font = font)
    text = "would like to change the number of beats per measure. The " +\
           "default is 4."
    canvas.create_text(w/2, h/4 + 60, text = text, font = font)
    text = "You will then be prompted to enter a note letter. Note letters" + \
           " include 'a' , 'b' , 'c' ,"
    canvas.create_text(w/2, h/4 + 75, text = text, font = font)
    text =  " 'd' , 'e' , 'f' , 'g' . You can also designate how long a note "+\
            "lasts" +\
            " by putting a '-'."
    canvas.create_text(w/2,h/4 + 90, text = text, font = font)
    text = "You can also add rests by pressing '.' ." + \
           " Then, select which clef you want your score to be in."
    canvas.create_text(w/2,h/4 + 105, text= text,font=font)
    canvas.create_image(w/2,h/4 + 135, image = data.helpScreen2)
    text = "If you are in the score, you can edit your text directly by "+\
           "typing the notes that you would like to add."
    canvas.create_text(w/2,h/4 + 160, text = text, font = font)
    text = "You can also press backspace to remove rests and notes. The " +\
           "program knows how to deal with these situations."
    canvas.create_text(w/2,h/4 + 175, text= text, font= font)
    text = "If you would like to return to the previous menu where you can"+\
           " change the beats and type, press 'Main Menu'"
    canvas.create_text(w/2,h/4 + 190, text =text, font =font)
    text = " and then you click 'Create Your Own Music Score'"
    canvas.create_text(w/2,h/4 + 205, text= text, font = font)
    canvas.create_image(w/2,h/4 + 235, image = data.helpScreen3)
    text = "To animate or play your score, you must have built a score first."+\
           " After you are done with that,"
    canvas.create_text(w/2,h/4 + 250, text= text, font = font)
    text = "On the score screen, you will see two options at the bottom: " +\
           "Animate, Play. Select animate to see your song roll"
    canvas.create_text(w/2,h/4 + 265, text =text, font = font)
    text = "across the screen. Select play to play the song." +\
           " In the animate bar, you also have the option to"
    canvas.create_text(w/2,h/4 + 280, text=text,font = font)
    text = "play your music. This will play your music and animate at the " +\
           "same time."
    canvas.create_image(w/8, 7*h/8, image = data.mainmenu)
    data.mmPos = w/8, 7*h/8

def drawBackButton(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(w/2,7*h/8,image =data.backImage)
    data.biPos = (w/2,7*h/8)

def drawCreateYour(data, canvas):
    w,h = data.width,data.height
    canvas.create_image(w/2,h/8,image = data.createyour)

def drawStartUpLogo(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(w/2, h/8, image=data.logo)
    canvas.create_image(w/2 + 1, h/8 + 1, image=data.logo)

def drawStartUpOptions(data,canvas):
    w,h = data.width,data.height
    cx = w/2
    barrier = h/8
    image = data.createtext
    canvas.create_image(cx, barrier + 100, image = image)
    data.ctPos = cx,barrier+100
    image = data.help
    canvas.create_image(cx, barrier + 150, image = image)
    data.hPos = cx,barrier +150
    for measure in data.startUpMeasures:
        measure.draw(canvas)
        measure.drawLines(canvas)
    for note in data.startUpNotesList:
        note.draw(canvas,data)

def randomizeNotesForStartUpMeasures(data):
    noteLimit = 4000
    noteStr = ''
    for i in range(noteLimit):
        randomNoteLetter = random.choice(['a','b','c','d','e','f','g'])
        randomNoteHold = random.choice(['','-','--'])
        if(randomNoteLetter == "."): randomNoteHold = ''
        noteStr += randomNoteLetter + randomNoteHold
    data.startUpNotes = noteStr
    updateStartUpNoteList(data)

#All of the cooltext (images) were from cooltext.com
def init(data):
    data.createyour = PhotoImage(file = "Images/createyour.gif")
    data.play = PhotoImage(file = "Images/play.gif")
    data.pWidth,data.pHeight = 107,52
    data.pPos = (0,0)
    data.youhavetypedsmall = PhotoImage(file="Images/youhavetypedsmall.gif")
    data.image = PhotoImage(file="Images/qrest.gif")
    data.halfImage = data.image.subsample(20,20)
    data.image = data.halfImage
    data.logo = PhotoImage(file="Images/logo.gif")
    data.logo2 = PhotoImage(file = "Images/logo2.gif")
    data.createtext = PhotoImage(file = "Images/createtext.gif")
    data.youHaveTyped = PhotoImage(file = "Images/youhavetyped.gif")
    data.orgct = data.createtext
    data.createtext2 = PhotoImage(file = "Images/createtext2.gif")
    data.helpScreen = PhotoImage(file = "Images/helpScreen.gif")
    data.helpScreen1 = PhotoImage(file = "Images/help1.gif")
    data.ctWidth = 409
    data.ctHeight = 55
    data.ctPos = (0,0)
    data.hPos = (0,0)
    data.help = PhotoImage(file = "Images/help.gif")
    data.orghelp = data.help
    data.help2 = PhotoImage(file = "Images/help2.gif")
    data.helpAnimate = False
    data.hWidth = 97
    data.hHeight = 47
    data.ctAnimate = False
    data.startUpMeasures = buildMeasureLine(data,10,600,100)
    data.startUpNotesList = []
    data.startUpNotes = ''
    data.measureList = []
    data.measureIndex = 0
    buildAllMeasures(data)
    data.noteList = []
    data.currNote = 0
    data.song = ''
    data.currMeasureBeats = 4
    data.realCurrMeasureBeats = data.currMeasureBeats
    data.changeScreen = False
    data.onText = False
    data.window = 1
    data.motionPosn = (data.width//2, data.height//2)
    data.leftPosn = (data.width//4, data.height//2)
    data.mmPos = (0,0)
    data.mainmenu = PhotoImage(file = 'Images/mainmenu.gif')
    data.mainmenu2 = PhotoImage(file = 'Images/mainmenu2.gif')
    data.mmanimate = False
    data.orgmm = data.mainmenu
    data.mmWidth,data.mmHeight = 189,47
    data.backImage = PhotoImage(file = "Images/back.gif")
    data.biPos = (0,0)
    data.biWidth,data.biHeight = 109,52
    data.noteIndex = 0
    data.animateSong = False
    data.animationMeasureList = []
    data.animationNoteList = []
    data.trebleClef = PhotoImage(file = "Images/TrebleClef.gif")
    data.trebleClef = data.trebleClef.subsample(40,40)
    data.tClefPos = (0,0)
    data.bassClef = PhotoImage(file = "Images/BassClef.gif")
    data.bassClef = data.bassClef.subsample(10,10)
    data.bClefPos = (0,0)
    data.bassChoice = PhotoImage(file = "Images/Bass.gif")
    data.bcPos = (0,0)
    data.bcWidth, data.bcHeight = 71,37
    data.trebleChoice = PhotoImage(file = "Images/Treble.gif")
    data.tcPos = (0,0)
    data.tcWidth, data.tcHeight = 92,37
    data.chooseClef = PhotoImage(file = "Images/chooseClef.gif")
    data.clefChoice = ''
    data.bassChoicePos = (0,0)
    data.trebleChoicePos = (0,0)
    data.animateImage = PhotoImage(file = "Images/animate.gif")
    data.animatePos = (0,0)
    data.aiWidth,data.aiHeight = 149,55
    randomizeNotesForStartUpMeasures(data)
    data.playSong = False
    data.beats = PhotoImage(file = "Images/setBeats.gif")
    data.beatsPos = (0,0)
    data.beatsWidth,data.beatsHeight = 385,55
    data.beatsTitle = PhotoImage(file = "Images/setBeatsTitle.gif")
    data.beat1 = PhotoImage(file = "Images/beat1.gif")
    data.b1Pos = (0,0)
    data.b1Height,data.b1Width = 38,47
    data.beat2 = PhotoImage(file = "Images/beat2.gif")
    data.b2Pos = (0,0)
    data.b2Height,data.b2Width = 43,47
    data.beat3 = PhotoImage(file = "Images/beat3.gif")
    data.b3Pos = (0,0)
    data.b3Height,data.b3Width = 44,47
    data.beat4 = PhotoImage(file = "Images/beat4.gif")
    data.b4Height,data.b4Width = 43,47
    data.b4Pos = (0,0)
    data.helpScreen2 = PhotoImage(file = "Images/helpScreen2.gif")
    data.helpScreen3 = PhotoImage(file = "Images/helpScreen3.gif")
    data.tempo = 100
    data.title = ''
    data.titleImage = PhotoImage(file = "Images/title.gif")
    data.titlePos = (0,0)
    data.titleWidth,data.titleHeight = 167,55
    data.submit = PhotoImage(file = "Images/submit.gif")
    data.submitPos = (0,0)
    data.submitWidth,data.submitHeight = 213,55

def drawBeatsSelectionWindow(data,canvas):
    w,h = data.width,data.height
    canvas.create_image(w/2,h/8,image = data.beatsTitle)
    canvas.create_image(w/5,h/2,image = data.beat1)
    data.b1Pos = (w/5, h/2)
    canvas.create_image(2*w/5,h/2,image = data.beat2)
    data.b2Pos = (2*w/5, h/2)
    canvas.create_image(3*w/5,h/2,image = data.beat3)
    data.b3Pos = (3*w/5, h/2)
    canvas.create_image(4*w/5,h/2,image = data.beat4)
    data.b4Pos = (4*w/5, h/2)

def drawTitleWindow(data,canvas):
    w,h = data.width,data.height
    cx,cy = data.width/2, data.height/2
    xRadius = 100
    yRadius = 10
    canvas.create_rectangle(cx-xRadius,cy-yRadius,cx+xRadius, cy+yRadius)
    canvas.create_text(cx,cy,text = data.title[:37])
    canvas.create_image(cx, cy + 3*yRadius, image = data.submit)
    data.submitPos = cx,cy + 3*yRadius

def drawTitle(data,canvas):
    w,h = data.width,data.height
    font = "Monaco 40"
    text = "Playing " + data.title[:37]
    canvas.create_text(w/2,h/8, text = text, font = font)

def drawTrebleClef(data,canvas, measure):
    x = measure.x0
    y = (measure.y0 +measure.y1)//2 + 10
    data.tClefPos = (x,y)
    canvas.create_image(x,y,image = data.trebleClef,anchor = "w")

def drawBassClef(data,canvas, measure):
    x = measure.x0 + 2
    y = (measure.y0 +measure.y1)//2 - 5
    data.bClefPos = (x,y)
    canvas.create_image(x,y,image = data.bassClef,anchor = "w")

def moveBassClef(data):
    x,y = data.bClefPos
    x+=1
    y+=1
    data.bClefPos = x,y

def moveTrebleClef(data):
    x,y = data.tClefPos
    x+=1
    y+=1
    data.tClefPos = x,y

def initializeAnimationMeasuresAndNotes(data):
    data.animationMeasureList = buildMeasureLine(data,data.width,data.height//2,
                                                 len(data.measureList))
    updateAnimationNoteList(data)

def mousePressed(event, data):
    data.motionPosn = (event.x, event.y)
    if(data.window == 1):
        ctcx,ctcy = data.ctPos
        deltaX, deltaY = data.ctWidth//2, data.ctHeight//2
        if(event.x >= ctcx - deltaX and event.x <= ctcx + deltaX and
           event.y >= ctcy - deltaY and event.y <= ctcy + deltaY):
            data.window += 1

        hcx,hcy = data.hPos
        deltaX, deltaY = data.hWidth//2, data.hHeight//2
        if(event.x >= hcx - deltaX and event.x <= hcx + deltaX and
           event.y >= hcy - deltaY and event.y <= hcy + deltaY):
            data.window += 2
    if(data.window == 2):
        mmcx,mmcy = data.mmPos
        deltaX, deltaY = data.mmWidth//2, data.mmHeight//2
        if(event.x >= mmcx - deltaX and event.x <= mmcx + deltaX and
           event.y >= mmcy - deltaY and event.y <= mmcy + deltaY):
            data.window -= 1
            data.animateSong = False
            data.changeScreen = False
            data.clefChoice = ''
        if(data.changeScreen and not data.animateSong):
            aicx,aicy = data.animatePos
            deltaX, deltaY = data.aiWidth//2, data.aiHeight//2
            if(event.x >= aicx - deltaX and event.x <= aicx + deltaX and
               event.y >= aicy - deltaY and event.y <= aicy + deltaY):
                initializeAnimationMeasuresAndNotes(data)
                data.animateSong = True
                if(data.song == ''): data.animatedNoteList = []
            pcx,pcy = data.pPos
            deltaX, deltaY = data.pWidth//2, data.pHeight//2
            if(event.x >= pcx - deltaX and event.x <= pcx + deltaX and
               event.y >= pcy - deltaY and event.y <= pcy + deltaY):
                if(len(data.song)>0):
                    playSongs(data)
        elif(data.animateSong):
            pcx,pcy = data.pPos
            deltaX, deltaY = data.pWidth//2, data.pHeight//2
            if(event.x >= pcx - deltaX and event.x <= pcx + deltaX and
               event.y >= pcy - deltaY and event.y <= pcy + deltaY):
                if(len(data.song)>0):
                    data.playSong = True
            bicx,bicy = data.biPos
            deltaX, deltaY = data.biWidth//2, data.biHeight//2
            if(event.x >= bicx - deltaX and event.x <= bicx + deltaX and
               event.y >= bicy - deltaY and event.y <= bicy + deltaY):
                data.animateSong = False
        else:
            titlecx,titlecy = data.titlePos
            deltaX, deltaY = data.titleWidth//2, data.titleHeight//2
            if(event.x >= titlecx - deltaX and event.x <= titlecx + deltaX and
               event.y >= titlecy - deltaY and event.y <= titlecy + deltaY):
                data.window = 5
            tccx,tccy = data.tcPos
            deltaX, deltaY = data.tcWidth//2, data.tcHeight//2
            if(event.x >= tccx - deltaX and event.x <= tccx + deltaX and
               event.y >= tccy - deltaY and event.y <= tccy + deltaY):
                data.changeScreen = True
                data.clefChoice = data.trebleClef
                updateNoteList(data)
            bccx,bccy = data.bcPos
            deltaX, deltaY = data.bcWidth//2, data.bcHeight//2
            if(event.x >= bccx - deltaX and event.x <= bccx + deltaX and
               event.y >= bccy - deltaY and event.y <= bccy + deltaY):
                data.changeScreen = True
                data.clefChoice = data.bassClef
                updateNoteList(data)
            beatscx,beatscy = data.beatsPos
            deltaX, deltaY = data.beatsWidth//2, data.beatsHeight//2
            if(event.x >= beatscx - deltaX and event.x <= beatscx + deltaX and
               event.y >= beatscy - deltaY and event.y <= beatscy + deltaY):
                data.window += 2

    if(data.window == 3):
        mmcx,mmcy = data.mmPos
        deltaX, deltaY = data.mmWidth//2, data.mmHeight//2
        if(event.x >= mmcx - deltaX and event.x <= mmcx + deltaX and
           event.y >= mmcy - deltaY and event.y <= mmcy + deltaY):
            data.window -= 2

    if(data.window == 4):
        b1cx,b1cy = data.b1Pos
        b2cx,b2cy = data.b2Pos
        b3cx,b3cy = data.b3Pos
        b4cx,b4cy = data.b4Pos
        deltaX, deltaY = data.b1Width//2, data.b1Height//2
        if(event.x >= b1cx - deltaX and event.x <= b1cx + deltaX and
           event.y >= b1cy - deltaY and event.y <= b1cy + deltaY):
            data.currMeasureBeats = 1
            data.window -= 2
            data.realCurrMeasureBeats = data.currMeasureBeats
        deltaX, deltaY = data.b2Width//2, data.b2Height//2
        if(event.x >= b2cx - deltaX and event.x <= b2cx + deltaX and
           event.y >= b2cy - deltaY and event.y <= b2cy + deltaY):
            data.currMeasureBeats = 2
            data.window -= 2
            data.realCurrMeasureBeats = data.currMeasureBeats
        deltaX, deltaY = data.b3Width//2, data.b3Height//2
        if(event.x >= b3cx - deltaX and event.x <= b3cx + deltaX and
           event.y >= b3cy - deltaY and event.y <= b3cy + deltaY):
            data.currMeasureBeats = 3
            data.realCurrMeasureBeats = data.currMeasureBeats
            data.window -= 2
        deltaX, deltaY = data.b4Width//2, data.b4Height//2
        if(event.x >= b4cx - deltaX and event.x <= b4cx + deltaX and
           event.y >= b4cy - deltaY and event.y <= b4cy + deltaY):
            data.currMeasureBeats = 4
            data.realCurrMeasureBeats = data.currMeasureBeats
            data.window -= 2
    if(data.window == 5):
        scx,scy = data.submitPos
        deltaX, deltaY = data.submitWidth//2, data.submitHeight//2
        if(event.x >= scx - deltaX and event.x <= scx + deltaX and
           event.y >= scy - deltaY and event.y <= scy + deltaY):
            data.window -= 3

def keyPressed(event, data):
    if(data.window == 2):
        if(event.keysym == 'BackSpace'):
            if(len(data.noteList) > 0) and type(data.noteList[-1]) == Note:
                data.noteList.pop()
            elif(len(data.noteList) > 0)  and type(data.noteList[-1]) != Note:
                changeNote(data)
            newIndex = len(data.song) - 1
            data.song = data.song[:newIndex]
        if(event.keysym in {'a','b','c','d','e','f','g','period','minus'}):
            obtainNotesFromUI(data,event)
        if(data.changeScreen):
            updateNoteList(data)
    if(data.window == 5):
        if(len(event.keysym) == 1):
            data.title += event.keysym
        elif(event.keysym == "space"):
            data.title += " "
        elif(event.keysym == 'BackSpace'):
            data.title = data.title[:len(data.title) - 1]

def changeNote(data):
    note = data.noteList.pop()
    x = note.x
    noteLetter = note.note
    measure = note.measure
    if(type(note) == HalfNote):
        note = Note(x,noteLetter,measure,data)
        data.noteList.append(note)
    if(type(note) == DottedHalfNote):
        note = HalfNote(x,noteLetter,measure,data)
        data.noteList.append(note)
    if(type(note) == WholeNote):
        note = DottedHalfNote(x,noteLetter,measure,data)
        data.noteList.append(note)

def updateNoteList(data):
    if(len(data.song) >0):
        data.noteList = []
        data.currMeasureBeats = data.realCurrMeasureBeats
        totalBeats = data.currMeasureBeats
        data.measureIndex = 0
        s = data.song
        data.song = ''
        newStr = ''
        for i in range(len(s)):
            newStr += s[i]
            if(i+1<len(s)):
                if(s[i+1] != "-"):
                    newStr += ","
        song = newStr.split(",")
        if(data.realCurrMeasureBeats == 1):
            beatsToNotes = {'':(Note,1)}
        elif(data.realCurrMeasureBeats == 2):
            beatsToNotes = {'':(Note,1),'-':(HalfNote,2)}
        elif(data.realCurrMeasureBeats == 3):
            beatsToNotes = {'':(Note,1),'-':(HalfNote,2),'--':(DottedHalfNote,3)
                            }
        elif(data.realCurrMeasureBeats == 4):
            beatsToNotes = {'':(Note,1),'-':(HalfNote,2),'--':
                            (DottedHalfNote,3),'---':(WholeNote,4)}
        spacing = data.measureList[0].getWidth()/5
        counter = 0
        for note in song:
            if(counter == len(beatsToNotes)):
                counter = 0
                data.measureIndex += 1
                data.currMeasureBeats = data.realCurrMeasureBeats
            if(data.currMeasureBeats == 0):
                data.currMeasureBeats = data.realCurrMeasureBeats
            mI = data.measureIndex
            while(len(note[1:]) > totalBeats -1):
                note = note[:len(note) -1]
            noteType,nBeats = beatsToNotes[note[1:]]
            currNote = note[0]
            if(len(data.song) != 0):
                if data.currMeasureBeats - nBeats < 0:
                #for the remaining beats put them as rests...
                    for i in range(counter,totalBeats):
                        note = "." + note
                        mI = data.measureIndex
                        newRest = Note(data.measureList[mI].x0 +
                                       (i+0.5)*spacing,
                                       '.',
                                       data.measureList[mI],data)
                        data.noteList.append(newRest)
                    data.measureIndex += 1
                    mI = data.measureIndex
                    data.currMeasureBeats = data.realCurrMeasureBeats
                    counter = 0
            if(data.measureIndex >= len(data.measureList)): break
            if(mI == 0):
                newNote = noteType(data.measureList[mI].x0 + 20 +
                                   (counter+0.5)*spacing,
                                   currNote,
                                   data.measureList[mI],data)
            else:
                newNote = noteType(data.measureList[mI].x0 +
                                   (counter+0.5)*spacing,
                                   currNote,
                                   data.measureList[mI],data)
            data.noteList.append(newNote)
            counter += nBeats
            data.currMeasureBeats -= nBeats
            data.song += note
            if data.measureIndex > len(data.measureList): break

def updateAnimationNoteList(data):
    if(len(data.song) > 0):
        data.animationNoteList = []
        data.currMeasureBeats = data.realCurrMeasureBeats
        totalBeats = data.currMeasureBeats
        data.measureIndex = 0
        s = data.song
        data.song = ''
        newStr = ''
        for i in range(len(s)):
            newStr += s[i]
            if(i+1<len(s)):
                if(s[i+1] != "-"):
                    newStr += ","
        song = newStr.split(",")
        beatsToNotes = {'':(Note,1),'-':(HalfNote,2),'--':(DottedHalfNote,3),
                        '---':(WholeNote,4)}
        spacing = data.animationMeasureList[0].getWidth()/5
        counter = 0
        for note in song:
            if(counter == data.realCurrMeasureBeats):
                counter = 0
                data.measureIndex += 1
                data.currMeasureBeats = data.realCurrMeasureBeats
            if(data.currMeasureBeats == 0):
                data.currMeasureBeats = data.realCurrMeasureBeats
            mI = data.measureIndex
            noteType,nBeats = beatsToNotes[note[1:]]
            currNote = note[0]
            if(len(data.song) != 0):
                if data.currMeasureBeats - nBeats < 0:
                #for the remaining beats put them as rests...
                    for i in range(counter,totalBeats):
                        note = "." + note
                        mI = data.measureIndex
                        newRest = Note(data.animationMeasureList[mI].x0 +
                                       (i+0.5)*spacing,
                                       '.',
                                       data.animationMeasureList[mI],data)
                        data.animationNoteList.append(newRest)
                    data.measureIndex += 1
                    mI = data.measureIndex
                    data.currMeasureBeats = data.realCurrMeasureBeats
                    counter = 0
            if(mI == 0):
                newNote = noteType(data.animationMeasureList[mI].x0 + 20 +
                                   (counter+0.5)*spacing,
                               currNote,
                               data.animationMeasureList[mI],data)
            else:
                newNote = noteType(data.animationMeasureList[mI].x0 +
                                   (counter+0.5)*spacing,
                               currNote,
                               data.animationMeasureList[mI],data)
            data.animationNoteList.append(newNote)
            counter += nBeats
            data.currMeasureBeats -= nBeats
            data.song += note
        data.animationMeasureList = data.animationMeasureList[:data.measureIndex
                                                               +1]

def updateStartUpNoteList(data):
    s = data.startUpNotes
    newStr = ''
    for i in range(len(s)):
        newStr += s[i]
        if(i+1<len(s)):
            if(s[i+1] != "-"):
                newStr += ","
    song = newStr.split(",")
    beatsToNotes = {'':(Note,1),'-':(HalfNote,2),'--':(DottedHalfNote,3),
                    '---':(WholeNote,4)}
    spacing = data.startUpMeasures[0].getWidth()/5
    counter = 0
    for note in song:
        if(counter == 4):
            counter = 0
            data.measureIndex += 1
            data.currMeasureBeats = 4
        if(data.currMeasureBeats == 0):
            data.currMeasureBeats = 4
        mI = data.measureIndex
        noteType,nBeats = beatsToNotes[note[1:]]
        totalBeats = 4
        currNote = note[0]
        if data.currMeasureBeats - nBeats < 0:
        #for the remaining beats put them as rests...
            for i in range(counter,totalBeats):
                mI = data.measureIndex
                newRest = Note(data.startUpMeasures[mI].x0 + (i+0.5)*spacing,
                               '.',
                               data.startUpMeasures[mI],data)
                data.startUpNotesList.append(newRest)
            data.measureIndex += 1
            mI = data.measureIndex
            data.currMeasureBeats = 4
            counter = 0
        if(data.measureIndex >= len(data.startUpMeasures)): break
        newNote = noteType(data.startUpMeasures[mI].x0 + (counter+0.5)*spacing,
                           currNote,
                           data.startUpMeasures[mI],data)
        data.startUpNotesList.append(newNote)
        counter += nBeats
        data.currMeasureBeats -= nBeats

def timerFired(data,canvas):
    if(data.animateSong):
        for measure in data.animationMeasureList:
            measure.onTimerFired(data)
        if(len(data.song) != 0):
            for i in range(len(data.animationNoteList)):
                note = data.animationNoteList[i]
                actualLetter = ''
                actualNote = ''
                noteLoc = ''
                note.onTimerFired(data)
                if(note.x == data.width//2):
                    notesDict = dict()
                    notesDict = mapNotesToFile(notesDict,data)
                    if(note.note != '.'):
                        noteLoc = notesDict[note.note]
                    notesToBeats = {Note:'',HalfNote:'-',DottedHalfNote:'--',
                                    WholeNote:'---'}
                    actualLetter = note.note
                    actualNote = actualLetter + notesToBeats[type(note)]
                    randomColor = random.choice(["blue","green","red"])
                    note.setColor(randomColor)
                    redrawAll(canvas,data)
                    if(data.playSong):
                        if(actualLetter != "."):
                            playNote(noteLoc,actualNote)
                        else:
                            time.sleep(0.5)
        else: data.animationNoteList = []
        lastIndex = len(data.animationMeasureList) -1
        if(data.animationMeasureList[lastIndex].x1 <= 0):
            initializeAnimationMeasuresAndNotes(data)

    if data.ctAnimate:
        animateImage(data)
    if data.helpAnimate:
        animateHelp(data)
    if data.mmanimate:
        animateMainMenu(data)
    if(data.window == 1 or data.window == 2) and (not data.changeScreen):
        for measure in data.startUpMeasures:
            measure.onTimerFired(data)
        for note in data.startUpNotesList:
            note.onTimerFired(data)

def mouseMotion(event, data):
    data.motionPosn = (event.x, event.y)
    if(data.window == 1):
        ctcx,ctcy = data.ctPos
        deltaX, deltaY = data.ctWidth//2, data.ctHeight//2
        if(event.x >= ctcx - deltaX and event.x <= ctcx + deltaX and
           event.y >= ctcy - deltaY and event.y <= ctcy + deltaY):
           data.ctAnimate = True
        else:
           data.ctAnimate = False
           if data.orgct != data.createtext:
               data.createtext,data.createtext2 = data.createtext2,\
                                                  data.createtext


        hcx,hcy = data.hPos
        deltaX, deltaY = data.hWidth//2, data.hHeight//2
        if(event.x >= hcx - deltaX and event.x <= hcx + deltaX and
           event.y >= hcy - deltaY and event.y <= hcy + deltaY):
           data.helpAnimate = True
        else:
           data.helpAnimate = False
           if data.orghelp != data.help:
               data.help,data.help2 = data.help2,data.help
    if(data.window == 2):
        mmcx,mmcy = data.mmPos
        deltaX,deltaY = data.mmWidth//2,data.mmHeight//2
        if(event.x >= mmcx - deltaX and event.x <= mmcx + deltaX and
           event.y >= mmcy - deltaY and event.y <= mmcy + deltaY):
           data.mmanimate = True
        else:
           data.mmanimate = False
           if data.orgmm != data.mainmenu:
               data.mainmenu,data.mainmenu2 = data.mainmenu2,data.mainmenu
    if(data.window == 3):
        mmcx,mmcy = data.mmPos
        deltaX,deltaY = data.mmWidth//2,data.mmHeight//2
        if(event.x >= mmcx - deltaX and event.x <= mmcx + deltaX and
           event.y >= mmcy - deltaY and event.y <= mmcy + deltaY):
           data.mmanimate = True
        else:
           data.mmanimate = False
           if data.orgmm != data.mainmenu:
               data.mainmenu,data.mainmenu2 = data.mainmenu2,data.mainmenu

def leftMoved(event, data):
    data.leftPosn = (event.x, event.y)

def animateImage(data):
    if(data.window == 1):
        data.createtext,data.createtext2 = data.createtext2,data.createtext

def animateHelp(data):
    if(data.window == 1):
        data.help,data.help2 = data.help2,data.help

def animateMainMenu(data):
    if(data.window == 3 or data.window == 2):
        data.mainmenu,data.mainmenu2 = data.mainmenu2,data.mainmenu

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data,canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def mouseWrapper(mouseFn, event, canvas, data):
        mouseFn(event, data)
        #redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds

    # create the root and the canvas (Note Change: do this BEFORE calling init!)
    root = Tk()

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    canvas.bind("<Motion>", lambda event:
                            mouseWrapper(mouseMotion, event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 800)
