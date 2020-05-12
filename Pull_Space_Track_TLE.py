import os
import pprint
import Tkinter
import time
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import Tk
import tkMessageBox
import tkSimpleDialog
from datetime import datetime
import subprocess
import sys
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"

now = datetime.now()
now_correct = now.strftime("%Y_%m_%d_%H_%M_%S")
root = Tk()
root.wm_attributes('-topmost', 1)

result = tkMessageBox.askyesno("Python",'''Hello, welcome to the automatic Space-Track 2 and 3 line element set downloader developed by Joshua Vaughan, TSOC Instructor.\n
This program will only work on the NIPRnet and will download a new and delightful copy of all the space object being tracked on Space-Track.org.\n
You will need a Space-Track.org username and password and you will have to have those handy.  If it is easier your team could probably share one username
and password.  If you have your username and password please click Yes to continue.''')

if result == True:
    pass
else:
    tkMessageBox.showinfo ("Program Aborted","You have chosen No, the program will now exit.")
    os._exit(0)

configUsr = tkSimpleDialog.askstring('Username', '''Please Enter your Space-Track.org Username, case sensitive.''')

configPwd = tkSimpleDialog.askstring('Password', '''Please Enter your Space-Track.org Password, case sensitive.''')

result = tkMessageBox.askyesno("Confirmation",'''You entered: ''' + configUsr + ''' as your Username.\nYou entered: ''' + configPwd + ''' as your Password.\n\n
Is this correct?''')

if result == True:
    pass
else:
    tkMessageBox.showinfo ("Program Aborted","You have chosen No, please run this program again and input the correct Username and Password")
    os._exit(0)

siteCred = {'identity': configUsr, 'password': configPwd}

with requests.Session() as session:
    resp = session.post(uriBase + requestLogin, data=siteCred)
    if resp.status_code != 200:
        tkMessageBox.showinfo("Log in Error", '''The Space-Track website returned something other than an HTTP 200 code which means
        that something went wrong, either Space-Track is down, your internet is down, or you put in your credentials wrong.  Run this program
        again and try it again.''')

    resp = session.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID/format/tle')
    if resp.status_code != 200:

        print "something has gone wrong"
        print resp.status_code

    resp2 = session.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/orderby/NORAD_CAT_ID/format/3le')
    if resp2.status_code != 200:
        print "something has gone wrong"
        print resp2.status_code

result = tkMessageBox.askyesno("File Directory",'''You will now select where you want your new TLE files to be saved. 
When you click "Yes" a box will pop up and you will use that to select where you want your new TLE file to be saved. 
If you do not understand click "No" and the program will be terminated.''')

if result == True:
    pass
else:
    tkMessageBox.showinfo ("Program Aborted","You have chosen No, Please get the requisite understanding of file directory selection and run this program again. Thank You.")
    os._exit(0)

directory = tkFileDialog.askdirectory()

os.chdir(directory)

answer1 = tkSimpleDialog.askstring('2 Line File Name', '''Please Enter the name for your 2 line Space-Track TLE, if you leave it empty an automatically chosen name will be generated.\n
Do not enter in the file extension ".txt" or the program will break, simply enter in the name of the file you would prefer.''')

if answer1 != '':
    pass
else:
    answer1 = 'Space_Track_2_line' + str(now_correct)

answer2 = tkSimpleDialog.askstring('3 Line File Name', '''Please Enter the name for your 3 line Space-Track TLE, if you leave it empty an automatically chosen name will be generated.\n
Do not enter in the file extension ".txt" or the program will break, simply enter in the name of the file you would prefer.''')

if answer2 != '':
    pass
else:
    answer2 = 'Space_Track_3_line' + str(now_correct)

write_file = open('placeholder.txt', 'w+')

for line in resp.iter_content(80):
    write_file.write(line)

write_file2 = open('placeholder2.txt', 'w+')

for line in resp2.iter_content(80):
    write_file2.write(line)

write_file.close()
write_file2.close()

remake_list = []

with open('placeholder.txt', 'r') as f:
    remake = f.readlines()

for line in remake:
    if line != '':
        remake_list.append(line.strip() + '\n')
    else:
        continue
remake_list2 = []
with open('placeholder2.txt', 'r') as g:
    remake2 = g.readlines()

for line in remake2:
    if line != '':
        remake_list2.append(line.strip() + '\n')
    else:
        continue

write_file_final = open(str(answer1) + '.txt', 'w+')

for s in remake_list:
    write_file_final.write(s)

write_file_final2 = open(str(answer2) + '.txt', 'w+')

for s in remake_list2:
    write_file_final2.write(s)

os.remove('placeholder.txt')
os.remove('placeholder2.txt')


write_file_final.close()
write_file_final2.close()
root.destroy()

tkMessageBox.showinfo("Program Completed",'''The program is now complete.  If you are seeing this message that means it all went well
and there will be a new 3 line element set sitting in the directory you chose at the beginning of this program.
The directory you chose was: \n\n''' + directory + '''\n\nPlease look there for your two new brand new and crispy Space-Track.org TLE files  
Please click ok to close this program.''')

os._exit(0)


