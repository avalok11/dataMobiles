#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 01. ask for file name, open it and save to variable

import re
import datetime



def userphone():
# look for phone number
# regular expression to finde the phone number - "Детализация оказанных услуг по Абонентскому номеру  +79113083788";;;;;;;;;;;;;
  reg_phone = re.compile(r'^\".+\s{2}\+(\d+)\";{13}')
# regular expression for real CSV - "01.12.15";;;"00:17:14";;"IN......
  csv_line = re.compile(r'^\"\d\d\.\d\d\.\d\d\".+')
# regular expression to delete -  "
  reg_quot = re.compile(r'"')
  return [reg_phone,csv_line, reg_quot]

# function to bring phone number (direction) to common view
# it shuld be 11 digits and start with 7
# function also determine the phone PREFIX and save it in arrary position [7]
# convert the date format from dd.mm.yy to yyyy.mm.dd
def preparecallstring(newline):
  shortnum=''
  newline[0]=datetime.datetime.strptime(newline[0],"%d.%m.%y").strftime("%Y-%m-%d")
  newline[3]=datetime.datetime.strptime(newline[3],"%H:%M:%S").strftime("%H:00")
  try:
    b=int(newline[5])
#    if len(newline[5])==10: newline[5] = '7' + newline[5]
    if len(newline[5])==11:
      string = list(newline[5])
      del string[0]
      newline[5] = ''.join(string)
      #print "NEW LINE", newline[5]
    if "Секунда"==newline[8]:
      #print newline[5], newline[8]
      newline[6]=str(int(newline[6])/60.0)
    if len(newline[5])>=11:
      if newline[5][0:2]=='00':
        string = list(newline[5])
        del string[0:2]
        newline[5] = ''.join(string)
      shortnum = newline[5][0:4]
    else:
      #переставить выше и сначала приамбулу дописать а потом определять оператора и регион и три цифры оператора
      if newline[10]=="Мурманск":
        shortnum = str(8152)
      elif newline[10]=="Столичный фил. ПАОМегаФон":
        shortnum = str(495)
      elif newline[10]=="Санкт-Петербург":
        shortnum = str(812)
      else: shortnum = str(0000)
    #newline[7]=shortnum
    if len(newline[5]) < 8: newline[5]=shortnum+newline[5]
  except:
    True
  return newline



def main():
# 01 ask for file name to read
  filename = raw_input("Enter the file name: ")
  if len(filename) < 3: filename = "januar-cp.csv"

# 02 try open the file
# create a new file (in this file will be saved our correct formatted data
  try:
    fh = open(filename)
    new_file = open("meg_new.txt", 'w')
  except:
    print "File not found: ", filename
    exit()

# 03 determine userphone, real csv line and quotes
  reg_phone = userphone()[0]
  csv_line = userphone()[1]
  reg_quot = userphone()[2]

# 04 start parsing the file
# first we need to find the user phone number "Детализация оказанных услуг по  Абонентскому номеру  +79113083788";;;;;;;;;;;;;
# then we will save the phone user number into variable "phone"
# ========
  for line in fh:
    phone = reg_phone.search(line)
    if phone: current_phone = phone.group(1)

# 05 find where real CSV start - "01.12.15";;;"00:17:14";;"IN
# clean the line:
# - remove \n in the end of string
# - remove quotas "
# - split line to ARRAY - > newline
# - add owner phone number to array
    if csv_line.search(line):
      newline = line.rstrip()
      newline = reg_quot.sub('', newline)
      newline = newline.split(';')
      newline[1] = current_phone

# change the 8 to 7 in phone number здесь я убил кучу времени, чтоб найти одну
# цифру и заменить ее на другую, поэтому просто закомментирую, но использовать
# не буду :)
#      nnline1 = reg_eight.sub(r'\g<1>7\g<2>', nnline, count=1)
#      nnline2 = reg_9_7.sub(r'\g<1>7\g<2>', nnline1, count=1)
# if we catch it -> split to list and put there fucking remebered phone number

# 06 prepare new line and make there a lot of modifications
      newline = preparecallstring(newline)

# 07 create string to put it in new file
      new_string=";".join(newline)
      new_file.write(new_string+"\n")
      #print new_string
#========
# finish parsing the file

# 08 save new file and close files
  fh.close()
  new_file.close()


if __name__ == '__main__':
    main()
