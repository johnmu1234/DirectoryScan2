import os
import sys, getopt
from datetime import datetime


class LogFileListClass:
    def __init__(self, name, timestamp):
        self.LogFilename = name
        self.LogTimeStamp = timestamp


class MatchRecord:
    def __init__(self, MatchString):
        self.MatchString = MatchString
        self.Count = 0


ArgListLen = len(sys.argv)
print("No of args " + str(ArgListLen))
for xx in range(ArgListLen):
    print(sys.argv[xx])

inputfile = ''
outputfile = 'temp.txt'
matchfile = 'match.txt'
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:m:o:")
except getopt.GetoptError:
    print('x.py -m <matchfile> -i <inputfile> -o <outputfile>')
    sys.exit(2)

print(opts)
print(args)
for opt, arg in opts:
    if opt == '-h':
        print('test.py -m <matchfile> -i <inputfile> -o <outputfile>')
        sys.exit()
    elif opt in ("-i"):
        inputfile = arg
    elif opt in ("-o"):
        outputfile = arg
    elif opt in ("-m"):
        matchfile = arg

print('Input file is ' + inputfile)
print('Output file is ' + outputfile)
print('Match file is ' + matchfile)

print("Dir: " + os.getcwd())
#os.setcwd("c:\\")
#print("Dir: " + os.getcwd())

# os.chdir('D:\\Sandboxes\\2_04_09\\Debug-28Aug18')
# print(os.getcwd())

MatchRecordList = []

if os.path.isfile(matchfile):
    # Open match file
    matchfile = open(matchfile, "r", encoding="utf-8")
    try:
        line = matchfile.readline()
        while line:
            print(line.strip())
            # Read lines into match list
            MatchRecordList.append(MatchRecord(line.strip()))
            line = matchfile.readline()
    finally:
        matchfile.close()
else:
    print("No 'match file' found")

ap2Count = 0
LogFileList = []

exists = os.path.isfile(outputfile)
if exists:
    os.remove(outputfile)

dirList = os.listdir()

print(dirList)
intList = []
for x in dirList:

    print("Str Found: " + x)
    if "LOG" in x:
        name, ext = x.split(".")
        #        print(x)
        #        print(name + "-" + ext)
        intTime = int(name, 16)
        #        print(intTime)
        intList.append(intTime)
        LogFileList.append(LogFileListClass(x, intTime))
    else:
        print(x + " not processed")

print("Log files found: " + str(len(LogFileList)))

LogFileList.sort(key=lambda x: x.LogTimeStamp, reverse=False)

try:
    outputfile = open(outputfile, "w", encoding="utf-8")
    for x in LogFileList:
        print(x.LogFilename + ", " + str(x.LogTimeStamp) + ", " + datetime.utcfromtimestamp(x.LogTimeStamp).strftime(
            '%Y-%m-%d %H:%M:%S'))

        inputfile = open(x.LogFilename, "r", encoding="utf-8")

        outputfile.write("=" * 60 + "\nLog file: " + x.LogFilename + " Start Time: '" + str(
            datetime.utcfromtimestamp(x.LogTimeStamp).strftime('%Y-%m-%d %H:%M:%S')) + "' {{ \n" + "=" * 60 + "\n")
        try:
            line = inputfile.readline()
            while line:
                try:
                    outputfile.writelines(line)
                except:
                    errLine = "\n\nFile Output Error " + str(sys.exc_info()[0]) + " " + x.LogFilename + "\n"
                    print(errLine)
                    outputfile.write(errLine)

                try:
                    line = inputfile.readline()

                    # For each in Match list
                    for ml in MatchRecordList:
                        if ml.MatchString in line:
                            ml.Count = ml.Count + 1
                        #                            print( ml.MatchString + "," + str(ml.Count) )
                        # if list item found in line, increment math list count

                        #                    if "AP2" in line:
                        #                        ap2Count = ap2Count + 1

                except:
                    errLine = "\n\nFile Input Error 1: " + str(sys.exc_info()[0]) + " " + x.LogFilename + "\n"
                    print(errLine)
                    outputfile.write(errLine)

            outputfile.write("}}\n")

        except:
            errLine = "\n\nFile Input Error: " + str(sys.exc_info()[0]) + " " + x.LogFilename + "\n"
            print(errLine)
            outputfile.write(errLine)
        finally:
            inputfile.close()

finally:
    if (MatchRecordList.__len__() > 0):
        outputfile.write("\nMatch results:\n")
        Count = 0
        for ml in MatchRecordList:
            outputfile.write('{:>3}'.format(Count) + '   {:50}'.format(ml.MatchString) + '{:4}'.format(ml.Count) + '\n')
            Count += 1
    outputfile.close()

# print("AP2 Count " + str(ap2Count))

if (MatchRecordList.__len__() > 0):
    print("\nMatch results:")
    Count = 0
    for ml in MatchRecordList:
        print('{:>3}'.format(Count) + '   {:50}'.format(ml.MatchString) + '{:4}'.format(ml.Count))
        Count += 1
