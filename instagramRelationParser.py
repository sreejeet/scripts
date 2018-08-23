import time
from pprint import pprint, pformat
import sys

username = sys.argv[1]
following = []
followers = []

# Log file
# Time formated for file name as YYYYMMDD-HHMMSS
log_time = time.localtime()
fileTime =	str(log_time.tm_year)\
+ str(log_time.tm_mon).zfill(2)\
+ str(log_time.tm_mday).zfill(2)\
+ "-"\
+ str(log_time.tm_hour).zfill(2)\
+ str(log_time.tm_min).zfill(2)\
+ str(log_time.tm_sec).zfill(2)

logFileName = username + '_' + fileTime + '.txt'
	
log = open('./files/' + logFileName, 'w', encoding='cp1252')

raw = open('followers_raw.txt', 'r', encoding='cp1252').read()
out = open('./files/' + username + '_followers_' + fileTime + '.txt', 'w', encoding='cp1252')
st = 0
en = 0
while True:
	st = raw.find('title="', en+1)
	en = raw.find('"', st+7)
	if en == -1 or st == -1:
		break;
	if raw[st+7:en] == 'Verified':
		continue;
	out.write(raw[st+7:en]+'\n')
	followers.append(raw[st+7:en])

raw = open('following_raw.txt', 'r', encoding='cp1252').read()
out = open('./files/' + username + '_following_' + fileTime + '.txt', 'w', encoding='cp1252')
st = 0
en = 0
while True:
	st = raw.find('title="', en+1)
	en = raw.find('"', st+7)
	if en == -1 or st == -1:
		break;
	if raw[st+7:en] == 'Verified':
		continue;
	out.write(raw[st+7:en]+'\n')
	following.append(raw[st+7:en])

followers_length = int(len(followers))
following_length = int(len(following))

log.write('Data for ' + username)

log.write('\nFollowers: ' + str(followers_length))
log.write('\nFollowing: ' + str(following_length))

if(followers_length == following_length):
	log.write('')
	print('Equal relations!!')
elif(followers_length > following_length):
	log.write('\n' + username + ' is followed by ' + str(followers_length - following_length) + ' more users.')
	print('Following ' + str(followers_length - following_length) + ' more.')
else:
	log.write('\n' + username + ' is following ' + str(following_length - followers_length) + ' more users.')
	print('Following ' + str(following_length - followers_length) + ' more.')

log.write('\n\n>>> In followers but not in following')
res = [str('\n' + x) for x in followers if x not in following]
log.write("\nCount: "+ str(len(res)))
print("Count: "+ str(len(res)))
for x in res:
	log.writelines(x)

#log.write('\n')
#log.write(pformat(res))

log.write('\n\n>>> In following but not in followers')
res = [str('\n' + x) for x in following if x not in followers]
log.write("\nCount: "+ str(len(res)))
print("Count: "+ str(len(res)))
for x in res:
	log.writelines(x)

print('Done!!\nCheck ' + logFileName + ' for details.')