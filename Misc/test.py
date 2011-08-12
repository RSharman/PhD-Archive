from psychopy import visual, event

myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
    fullscr=False, allowGUI=True, bitsMode=None)

message = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="Please press left or right to indicate whether")
                                                                                       
message.draw()
myWin.flip()
myWin.flip()

junk = event.waitKeys()