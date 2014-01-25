import sys
from time import sleep, time
import binascii
import glob
import os.path
def send(device, message):
	device.write(message)
	device.flush()
class Cue:
	def __init__(self, tm, msg):
		self.time = float(tm)
		self.message = msg
	def go(self, device, startTime):
		send(device, self.message)
		goTime = (time() * 1000 - startTime)
		print 'cue gone at %i, %i milliseconds off' % (goTime / 1000, self.time - goTime)
class Song:
	def __init__(self, ttl, cs):
		self.title = ttl
		self.cues = cs
	def play(self, device):
		initCue = 0
		if self.cues[0].time == 0:
			initCue = 1
		prompt = 'Ready to play ' + self.title + ', press enter to GO'
		raw_input(prompt)
		startTime = time() * 1000
		for cue in self.cues:
			cTime = cue.time
			sleep(max(0, (1000 * cTime) - startTime + 10))
			while (time() * 1000 - startTime) < cTime:
				continue
			cue.go(device, startTime)
		print 'Done with cues for %s!' % title
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
		send(self.midiOut, message)
	def rehearse(self):
		while True:
			self.printSongs()
			print 'Enter a number corrosponding to a song or anything else to exit'
			selection = raw_input('> ')
			if not(selection.isdigit() and int(selection) > 0 and int(selection) <= len(self.songs)):
				print 'Exiting rehearsal...'
				return 0
			self.songs[int(selection) - 1].play(self.midiOut)
	def show(self):
		startI = 0
		self.printSongs()
		print "Entering show mode.  Enter a valid index to start at an intermediate point, or nothing to start at the beginning"
		selection = raw_input('> ')
		if selection.isdigit() and int(selection) > 0 and int(selection) <= len(self.songs):
			startI = int(selection) - 1
		for song in self.songs[startI:]:
			song.play(self.midiOut)
	def loop(self):
		while True:
			print 'Please choose an option from below:'
			print '1. GOTO CUE'
			print '2. Rehearsal'
			print '3. Show'
			selection = input('> ')
			if isinstance(selection, int) and selection > 0 and selection <= 3:
				if selection == 1:
					self.goto()
				elif selection == 2:
					self.rehearse()
				elif selection == 3:
					self.show()

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
show.loop()
