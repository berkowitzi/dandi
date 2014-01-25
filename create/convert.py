import sys
import binascii
txChannel = '01'
cueIndex = 0
timeIndex = 1
if len(sys.argv) < 2:
	print 'Usage: python %s <input>' % sys.argv[0]
	sys.exit(1)
for line in open(sys.argv[1]):
	if line.startswith('#'):
		print line.rstrip().split(',')[0]
		continue
	opCode = '01'
	splitLine = line.rstrip().split(',')
	time = splitLine[timeIndex].split(':')
	minutes = int(time[0])
	seconds = 0
	if len(time) > 1:
		seconds = float(time[1])
	milliseconds = ((60 * minutes) + seconds) * 1000
	cueCode = binascii.hexlify(splitLine[cueIndex])
	cueCode = " ".join(cueCode[i:i+2] for i in range(0, len(cueCode),2))
	cueStack = 1
	if (len(splitLine)) > 2 and splitLine[2]:
		cueStack = int(splitLine[2])
		if cueStack > 9:
			print 'Invalid cue stack (%i)' % cueStack
		sys.exit(1)
	cueStackCode = binascii.hexlify(str(cueStack))
	output = 'F0 7F ' + txChannel + ' 02 01 ' + opCode + ' ' + cueCode + ' 00 ' + cueStackCode + ' F7'
	print '%i\t%s\t%s' % (milliseconds, output, splitLine[cueIndex])
