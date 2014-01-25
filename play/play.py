import sys
from time import sleep
import binascii
import glob
import os.path
class Cue:
	def __init__(self, tm, msg):
		self.time = tm
		self.message = msg
class Song:
	def __init__(self, ttl, cs):
		self.title = ttl
		self.cues = cs
class Show:
	title = ''
	songs = []
	def printSongs(self):
		for ind, song in enumerate(self.songs):
			print '(%i) %s' % (ind + 1, song.title)
	def __init__(self, filename, device):
		self.midiOut = open(device, 'w')
		self.title = filename.split('.')[0]
		currentCues = []
		songTitle = ''
		for line in open(sys.argv[1]):
			line = line.rstrip()
			if line.startswith('#'):
				if currentCues:
					self.songs.append(Song(songTitle,currentCues))
				songTitle = line[1:]
				currentCues = []
				continue
			splitLine = line.split('\t')
			time = int(splitLine[0])
			message = bytearray.fromhex(splitLine[1])
			currentCues.append(Cue(time,message))
		if currentCues:
			self.songs.append(Song(songTitle,currentCues))
	def goto(self):
		validInput = False
		cueStack = 1
		cue = -1
		while not validInput:
			ui = input("GOTO CUE: ")
			try:
				cue = float(ui)
			except TypeError:
				continue
			validInput = True
		cueCode = binascii.hexlify(str(cue))
		output = 'F07F01020101' + cueCode + '0031F7'
		message = bytearray.fromhex(output)
		self.midiOut.write(message)
	def rehearse(self):
		self.printSongs()
		validInput = False
		res = -1
		while not validInput:
			print 'Enter a number corrosponding to a song:'
			selection = input('> ')
			if isinstance(selection, int) and selection > 0 and selection <= len(self.songs):
				validInput = True
				res = selection
			else:
				print 'Invalid Input'
potentialDevices = glob.glob('/dev/midi*')
if not len(potentialDevices):
	print 'No MIDI devices have been detected'
	sys.exit(1)
device = ''
if len(potentialDevices) == 1:
	device = potentialDevices[0]
if len(potentialDevices) > 1:
	print 'Multiple MIDI devices have been detected, please select your desired device'
	for idx, dev in enumerate(potentialDevices):
		print '(%i) %s' % (idx + 1, dev)
	selected = 0
	validInput = False
	while not validInput:
		try:
			selected = int(input('> '))
		except TypeError:
			continue
		if selected > 0 and selected <= len(potentialDevices):
			validInput = True
	device = potentialDevices(selected - 1)
if len(sys.argv) < 2:
	print 'Usage: python %s <CommandFile>' % sys.argv[0]
	sys.exit(1)
if not os.path.isfile(sys.argv[1]):
	print 'Input file does not exist'
	sys.exit(1)
show = Show(sys.argv[1], device)
show.rehearse()
