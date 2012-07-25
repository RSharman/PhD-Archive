#Testing boots data

from psychopy import gui, core
import cPickle

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

fileName = str(files)
print fileName
pkl_file = open(fileName, 'rb')
data1 = cPickle.load(pkl_file)
print len(data1['bootLumPositions'])

pkl_file.close()
