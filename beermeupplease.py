from instapy import InstaPy
import time
import pickle
import random
import argparse
import sys
import re
from InstagramAPI import InstagramAPI
from datetime import datetime
from stop_words import get_stop_words
import string
import time

username = 'beer.me.up.please'
pwd = sys.argv[1]
user_id  = '32123147'

#post_time=float('1540901493')
#text=u'Finally found a can of the  @northernmonk and @finbackbrewery collaboration at @doctors_orders_ \U0001f60a\n\nOnce, Twice, Three times a whale is an incredible DIPA that was hazy and full of hoppy, fruity mango flavours - fully justified the price tag and at 8.2% did well to hide its strength. Really enjoyed this \U0001f64c\U0001f37b\U0001f44c\n.\n.\n.\n.\n.\n.\n.\n.\n.\n#craftbeer #beerporn #beerstagram #instabeer #beergeek #ipa #craftbeerporn #beer #beertography #beernerd #beerlover #craftbeerlife #craftbeernotcrapbeer #beerme #beersnob #beergasm #drinklocal #dipa #craftbeerlover #lionelrichie #craftbrew #craftnotcrap #brewery #indiapaleale #beersofinstagram #hophead #hops #craftbeergeek #craftbeerjunkie #craftipa'



API = InstagramAPI(username,pwd)
API.login()
API.getUsernameInfo(user_id)
API.LastJson

feed = API.getTotalSelfUserFeed()
i=0
for post in feed:
	post_text=post['caption']['text']
	post_time=post['caption']['created_at_utc']
	post_image=post['image_versions2']['candidates'][0]['url']
	sep='\n.\n.'

	pre_hashtags=''.join((c for c in post_text.split(sep)[0] if 0 < ord(c) < 127)).replace('\n','').split(' ')

	stop_words = list(get_stop_words('en'))
	url_words=' '.join([w for w in pre_hashtags if not w in stop_words][:10])
	no_punct=re.sub(r"[.,?!/]", "",url_words)
	url_string=re.sub(r" +",'-',no_punct)

	post_name=time.strftime('%Y-%m-%d', time.localtime(post_time))+'-'+url_string.lower()+".md"

	f = open('temp/_posts/'+post_name, "a")
	f.write('---\nlayout: post\nauthor: Lewis Gavin\n---\n\n')
	f.write("![latest craft beer"+url_words+"](" + post_image + ")\n\n")
	f.write(post_text.encode('utf-8'))
	f.close()

	i=i+1

	if i > 60:
		break

print("finished")
