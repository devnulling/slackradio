import time
from slackclient import SlackClient
import json
from urlparse import urlparse, parse_qs
import re
import os
import subprocess
import thread

def clean_str(str):
	str = str.replace(">", "")
	str = str.replace("<", "")
	return str

def find_youtube(text):
	match = re.search(r"youtube\.com/.*v=([^&]*)", text)
	if match:
		return match.group(1)
	else:
		return None

def download_youtube(code):
	url = str("http://www.youtube.com/watch?v=" + code)
	print "Downloading URL: ",url
	subprocess.call(['/usr/local/bin/youtube-dl', '-x', '--audio-format', 'wav', '-q', '--exec', '/home/node/demo/slackradio/post.py', '-o', '%(id)s.%(ext)s', url])

token = "" # get a token at https://api.slack.com/
sc = SlackClient(token)

if sc.rtm_connect():
	while True:
		result = sc.rtm_read()

		print result
		if result is not None:
			for item in result:
				if item.has_key('text'):
					cstr = clean_str(item['text'])
					youtube = find_youtube(cstr)
					print "Regex'd a Youtube: ", youtube
					thread.start_new_thread(download_youtube, (youtube,))
		time.sleep(1)
else:
	print "Connection Failed, invalid token?"