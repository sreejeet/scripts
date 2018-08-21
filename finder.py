#python 3.6
import time
import sys
import os

# Shell execution guide
# python finder.py  /path/to/folder/recursive/search key_file.txt 

start_time = str(time.ctime())
a = time.localtime()

# Time format for log file name YYYMMDD-HHMMSS
x =	str(a.tm_year)\
	+ str(a.tm_mon).zfill(2)\
	+ str(a.tm_mday).zfill(2)\
	+ "-"\
	+ str(a.tm_hour).zfill(2)\
	+ str(a.tm_min).zfill(2)\
	+ str(a.tm_sec).zfill(2)

try:
	#Search keyword file
	with open(sys.argv[2]) as f:
		searchList = f.read().splitlines()

	#Creating logging file

	log = open(
		'/finder_log_'
		+ x
		+ ".txt", 'w', encoding='utf-8')

# If error: printing Exception and exiting
except Exception as err:
	print(str(err) + '\nexiting...')
	exit()

log.write("At " + str(time.ctime()) + ", Searching for[")

keyDict = {}
for key in searchList:
	keyDict.update( {key:0} )
	log.write("\n\t" + key)

log.write("\n]\nBegining search...")

fileCounuter = 0

for (filePath, b, fileList) in os.walk(sys.argv[1]):
	for fileName in fileList:
	
		# Ignore previously created logs
		if(fileName[:11] == 'finder_log_'):
			continue
		
		# Opening file to search
		file = open(os.path.join(filePath, fileName), 'r', encoding='utf-8')
		try:
			file = str(file.read())
		except UnicodeDecodeError as err:
			# Skipping to next file if this file is unreadable
			print("Error Reading file: "\
				+ fileName\
				+ "\n" + str(err))
			continue
		
		print("[Searching in  \"" + fileName + "\"" + "]")
		# Uncomment this line for logging searched files
		# log.write("\n[Searching in  \"" + fileName + "\"" + "]")
		tmp = "\n"

		# Searching inside current file 'fileName'
		pos = -1
		fileCounuter += 1
		for key in searchList:
			cnt = 0
			while(True):
				pos = file.lower().find(key, pos+1)
				if(pos == -1):
					break
				else:
					keyDict[key] += 1
					try:
						# cnt += 1
						log.write("\nFound \"" + key + "\" in " + fileName
							+ "\n-----Start snippet-----\n"
							+ file[pos-50:pos+50]
							+ "\n------End snippet------\n\n")
					except UnicodeEncodeError as err:
						print("[Recording error] " + str(err) + " for " + key)
						log.write("\nRecording error " + str(err) + " for " + key)

log.write("\Ending search...\nFinal tally:")

log.write("\n" + str(fileCounuter).zfill(5) + " files searched.")
print("\n-------Statistics-------")
print(str(fileCounuter) + " files searched.")

# Logging search statistics
for x in keyDict:
	log.write("\n" + str(str(keyDict[x]).zfill(6)) + " : " + str(x))
	print(str(keyDict[x]).zfill(6) + " : " + str(x))

log.write("\n[End of search]")
print("[End of search]\n")
exit()
