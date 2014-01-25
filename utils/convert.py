import sys
import binascii
txChannel = '01'
if len(sys.argv) < 2:
	print 'Usage: python %s <input>' % sys.argv[0]
	sys.exit(1)
for line in open(sys.argv[1]):
	opCode = '01'
	splitLine = line.rstrip().split(',')
	time = splitLine[0].split(':')
	minutes = int(time[0])
	seconds = 0
	if len(time) > 1:
		seconds = float(time[1])
	milliseconds = ((60 * minutes) + seconds) * 1000
	cueCode = binascii.hexlify(splitLine[1])
	cueCode = " ".join(cueCode[i:i+2] for i in range(0, len(cueCode),2))
	cueStack = 1
	if (len(splitLine)) > 2 and splitLine[2]:
		cueStack = int(splitLine[2])
		if cueStack > 99:
			print 'Invalid cue stack (%i)' % cueStack
		sys.exit(1)
	cueStackCode = str(cueStack).zfill(2)
	output = 'F0 7F ' + txChannel + ' 02 01 ' + opCode + ' ' + cueCode + ' 00 ' + cueStackCode + ' F7'
	print '%i\t%s' % (milliseconds, output)
