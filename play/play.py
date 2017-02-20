import sys
from time import sleep, time
import rtmidi_python as rtmidi
import binascii
import glob
import os.path
delimiter = '***************************************************'
if len(sys.argv) < 2:
	print 'Usage: python %s <CommandFile>' % sys.argv[0]
	sys.exit(1)
if not os.path.isfile(sys.argv[1]):
	print 'Input file does not exist'
	sys.exit(1)
def send(device, message):
	device.send_message(message)
class Cue:
	def __init__(self, tm, msg, cn):
		self.time = float(tm)
		self.message = msg
		self.description = cn
	def go(self, device, startTime):
		send(device, self.message)
		goTime = (time() * 1000 - startTime)
		print 'cue %s at %.3fs' % (self.description, goTime / 1000)
class Song:
	def __init__(self, ttl, cs, ind):
		self.title = ttl
		self.cues = cs
		self.index = ind
	def play(self, device):
		prompt = 'Ready to play ' + self.title + ', press enter to GO'
		try:
			raw_input(prompt)
			startTime = time() * 1000
			for cue in self.cues:
				cTime = cue.time
				sleep(max(0, (1000 * cTime) - startTime + 10))
				while (time() * 1000 - startTime) < cTime:
					continue
				cue.go(device, startTime)
		except:
			print 'Discontinuing cue playback for %s...' % self.title
			print delimiter
			return
		print 'Done with cues for %s!' % self.title
		print delimiter
class Show:
	title = ''
	songs = []
	def printSongs(self):
		print delimiter
		print self.title
		print delimiter
		for ind, song in enumerate(self.songs):
			print '(%i) %s' % (ind + 1, song.title)
		print delimiter + '\n'
	def __init__(self, filename, device):
		self.title = filename.split('.')[0]
		currentCues = []
		songTitle = ''
		for line in open(sys.argv[1]):
			line = line.rstrip()
			if line.startswith('#'):
				if currentCues:
					toAdd = Song(songTitle, currentCues, len(self.songs) + 1)
					self.songs.append(toAdd)
				songTitle = line[1:]
				currentCues = []
				continue
			splitLine = line.split('\t')
			time = int(splitLine[0])
			message = bytearray.fromhex(splitLine[1])
			description = splitLine[2]
			currentCues.append(Cue(time,message, description))
		if currentCues:
			self.songs.append(Song(songTitle,currentCues, len(self.songs) + 1))
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
		send(device, message)
	def rehearse(self):
		while True:
			self.printSongs()
			print 'Enter a number corrosponding to a song or anything else to exit'
			selection = raw_input('> ')
			if not(selection.isdigit() and int(selection) > 0 and int(selection) <= len(self.songs)):
				print 'Exiting rehearsal...'
				return 0
			self.songs[int(selection) - 1].play(device)
	def show(self):
		startI = 0
		self.printSongs()
		print "Entering show mode.  Enter a valid index to start at an intermediate point, or nothing to start at the beginning"
		selection = raw_input('> ')
		if selection.isdigit() and int(selection) > 0 and int(selection) <= len(self.songs):
			startI = int(selection) - 1
		for song in self.songs[startI:]:
			song.play(device)
	def loop(self):
		while True:
			print 'Please choose an option from below:\n'
			print '1. GOTO CUE'
			print '2. Rehearsal'
			print '3. Show\n'
			selection = raw_input('> ')
			if selection.isdigit():
				selection = int(selection)
				if selection == 1:
					self.goto()
				elif selection == 2:
					self.rehearse()
				elif selection == 3:
					self.show()
				else: continue

device = rtmidi.MidiOut()
device.open_port(0)

show = Show(sys.argv[1], device)
show.loop()
'Exiting...'
