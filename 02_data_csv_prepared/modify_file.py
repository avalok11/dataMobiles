#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 01. ask for file name, open it and save to variable
#
#
#
#
#

import re


# ask for file name to read
def main():
  filename = raw_input("Enter the file name: ")
  if len(filename) < 3: filename = "januar-cp.csv"

# try open the file
  try:
    fh = open(filename)
  except:
    print "File not found: ", filename
    exit()

# create a new file (in this file will be saved our correct formated data
  new_file = open("meg_new.txt", 'w')

# look for phone number
# regular expression to finde the phone number - "Детализация оказанных услуг по Абонентскому номеру  +79113083788";;;;;;;;;;;;;
  reg_phone = re.compile(r'^\".+\s{2}\+(\d+)\";{13}')
# regular expression for real CSV - "01.12.15";;;"00:17:14";;"IN......
  csv_line = re.compile(r'^\"\d\d\.\d\d\.\d\d\".+')
# regular expression to delete -  "
  reg_quot = re.compile(r'"')

# start parsing the file
# first we need to find the user phone number "Детализация оказанных услуг по  Абонентскому номеру  +79113083788";;;;;;;;;;;;;
# then we will save the phone user number into variable "phone"
# ========
  for line in fh:
    phone = reg_phone.search(line)
    if phone:
# remeber phone number to put it in CSV new file
      current_phone = phone.group(1)
# print phone.group(1)
# =======

# find where real CSV start - "01.12.15";;;"00:17:14";;"IN
    csv = csv_line.search(line)
# if we catch it -> split to list and put there fucking remebered phone number
# remove \n in the end of string
    if csv:
      newline = csv.group().rstrip()
# remove " from string
      nnline = reg_quot.sub('', newline)
# change the 8 to 7 in phone number здесь я убил кучу времени, чтоб найти одну
# цифру и заменить ее на другую, поэтому просто закомментирую, но использовать
# не буду :)
#      nnline1 = reg_eight.sub(r'\g<1>7\g<2>', nnline, count=1)
#      nnline2 = reg_9_7.sub(r'\g<1>7\g<2>', nnline1, count=1)


# modify line to array/list
      newline = nnline.split(';')
# add current phone number to array
      newline[1] = current_phone

#print phone number (where to call)
#Change secondes to minutes (/60)
      shortnum=''
#      if int(newline[5]):
      try:
        b=int(newline[5])
        if len(newline[5])==10: newline[5] = '7' + newline[5]
        if len(newline[5])==11 and newline[5][0]=='8':
          string = list(newline[5])
          string[0] = '7'
          newline[5] = ''.join(string)
          print "NEW LINE", newline[5]
        if "Секунда"==newline[8]:
          print newline[5], newline[8]
          newline[6]=str(int(newline[6])/60.0)
#        if "Минута"==newline[8]:
#          print newline[5], newline[8]
        if len(newline[5])==11:
          shortnum = newline[5][0:4]
        else:
          if newline[10]=="Мурманск":
            shortnum = str(78152)
          elif newline[10]=="Столичный фил. ПАОМегаФон":
            shortnum = str(7495)
          elif newline[10]=="Санкт-Петербург":
            shortnum = str(7812)
          else: shortnum = str(0000)
        newline[7]=shortnum
        if len(newline[5]) < 8: newline[5]=shortnum+newline[5]
      except:
        True
      #  print "AA"

# create string to put it in new file
      new_string = ""
      for l in newline:
        new_string = new_string + l + ";"

      new_file.write(new_string+"\n")
      #print new_string

  fh.close()
  new_file.close()


if __name__ == '__main__':
    main()
