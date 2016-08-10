#!/usr/bin/python
import sys
import os
import subprocess

print "Playing Song: ", sys.argv[1]
code = sys.argv[1]
youtubecode = code.replace(" ", "")

cmd = '/usr/bin/python /home/node/demo/slackradio/slackradio.py --wavfile %s --gain 50' % youtubecode
print str(cmd)
os.system(str(cmd))
