#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def main():
  #ask for file name to read
  filename = raw_input("Enter the file name: ")
  if len(filename) < 3: filename = "megafonT.csv"

  #create a new file
  new_file = open("meg_new.txt",'w')

  #open the file
  try:
    fh = open(filename)
  except:
    print "File not found: ", filename
    exit()
  
  #look for phone number
  #here i will storre phone neumbers - phones
  phones = list()
  #regular expression to finde the phones - "Детализация оказанных услуг по Абонентскому номеру  +79113083788";;;;;;;;;;;;;
  reg_phone = re.compile(r'^\".+\s{2}\+(\d+)\";{13}')
  #regular expression for real CSV - "01.12.15";;;"00:17:14";;"IN......
  csv_line = re.compile(r'^\"\d\d\.\d\d\.\d\d\".+')
  #regular expression to delete -  "
  reg_quot = re.compile(r'"')
  #regular expression to modife 8812 to 7812 etc"
  reg_eight = re.compile(r'(\d\d;;)8(\d+;)')
  #regular expression to delete -  "
  reg_quot2 = re.compile(r'[{}]')

  for line in fh:
    phone = reg_phone.search(line)
    if phone:
      #remeber phone number to put it in CSV new file
      current_phone = phone.group(1)
      #print phone.group(1)

    #find where real CSV start - "01.12.15";;;"00:17:14";;"IN
    csv = csv_line.search(line)
    #if we catch it -> split to list and put there fucking remebered phone number
    if csv: 
      #remove \n in the end of string
      newline = csv.group().rstrip()
      #remove " from string
      nnline = reg_quot.sub('',newline)
      #chenge the 8 to 7 in phone number
#      print "FIRST================",nnline
      nnline1 = reg_eight.sub(r'\g<1>7\g<2>',nnline,count=1)
      #remove " from string
      #nnline1 = reg_quot2.sub('',nnline1)
#      print "SECOND===============",nnline1

      #modify line to array/list
      newline = nnline1.split(';')
      #add current phone number to array
      newline[1] = current_phone

      #create string to put it in new file
      new_string = ""
      for l in newline:
        new_string = new_string + l + ";"

      new_file.write(new_string+"\n")
      print new_string
      #print "\n"#
     
      #print newline




  fh.close()
  new_file.close()


if __name__ == '__main__':
    main()
