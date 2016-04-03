#!/usr/bin/env python
# -*- coding: utf-8 -*-


def file_open(filen):
  try:
    f_op = open(filen)
    return f_op
  except:
    print "File not found: ", filen
    exit()

def read_f(filen):
  a = list()
  for line in filen:
    text = line.decode('cp1251').encode('utf8')
    text = text.strip()
    a.append(text)
  return a

def poisk(ros_csv,operator,region):
  #print "I have started!!!"
  ret = [False]
  for line in ros_csv:
    newline = line.split(';')
    #print newline[0],newline[1],newline[2],newline[4]
          #operator=921
        #print int(newline[0])
    try:
      ros_op = int(newline[0])
      ros_reg1 = int(newline[1])
      ros_reg2 = int(newline[2])
      #print operator,region,"==", ros_op, ros_reg1, ros_reg2
      if operator==ros_op and region>ros_reg1 and region<ros_reg2:
  #    print phone_usr,"->",operator,region
        print "Operator: ",operator, newline[4], "Region: ", region, newline[5]
        ret = [True, line]
        break
    except:
      True
  return ret


def main():

# 01 ask for file name to read
  filename = raw_input("Enter the file name: ")
  if len(filename) < 3: filename = "meg_new.txt"
  csv_m = file_open(filename)
  new_file = open("meg_new_mod.txt", 'w')
  csv_ros_3 = file_open("Kody_ABC-3kh.csv")
  csv_ros_4 = file_open("Kody_ABC-4kh.csv")
  csv_ros_8 = file_open("Kody_ABC-8kh.csv")
  csv_ros_9 = file_open("Kody_DEF-9kh.csv")

  csv_ros3 = read_f(csv_ros_3)
  csv_ros4 = read_f(csv_ros_4)
  csv_ros8 = read_f(csv_ros_8)
  csv_ros9 = read_f(csv_ros_9)

  csv_ros_3.close()
  csv_ros_4.close()
  csv_ros_8.close()
  csv_ros_9.close()


# 02 prepare dict of variable and ROSSTAT file name
  csv ={'3':csv_ros3, '4':csv_ros4, '8': csv_ros8, '9':csv_ros9}

# 03 read Megafon csv file and get direction phone number [5]
  rosstat_data = list()
  for line_meg in csv_m:
    if "Минута" in line_meg or "Секунда" in line_meg:
      megafon = line_meg.split(";")
      if megafon[5]:
        phone_num = megafon[5]
      else: continue
      phone_num.split()
      phone_usr = megafon[1]
      try:
        operator = int(phone_num[:3])
        region = int(phone_num[3:])
        M = phone_num[0]
      except:
        True
#      print type(phone_num),operator,region

# 04 open rosstat csv file by direct phone number from megafon file
      temp = list()
      try:
        ros_csv = csv[M]
#        print "File is open: M"
      except:
        ros_csv = False #ЕСЛИ ФАЙЛА НУЖНОГО НЕТ ТО КАКОЙ ОПЕРАТОР И РЕГИОН?
        temp = ["",";;;;'ND';'ND';"]

# 05 its a testing
      '''operator = 900
      region = 1134567
      ros_csv = csv_ros9'''
# 05 read ROSSTAT files and dtermine Region and Operator name
      #print "User phone = ", phone_usr
      if ros_csv:
      #  print ""
      #  print 'Temporary data processing....'
        temp = poisk(rosstat_data,operator,region)
      #  print "Find in TEMPORARY dat:", temp[0]
        if temp[0]==False:
      #    print "CSV data processing:"
          temp=poisk(ros_csv,operator,region)
          if temp[0] == True:
            rosstat_data.append(temp[1])
          else:
            print " The number",operator,region,"not in the ROSSTAT file:", M
            temp = ["",";;;;'ND';'ND';"]

      megafon[4] = (temp[1].split(";")[4]).strip()
      megafon[7] = (temp[1].split(";")[5]).strip()
      print megafon[4], megafon[7]
      new_string=";".join(megafon)
      new_file.write(new_string)





# 09 coles files
  csv_m.close()
  new_file.close()

if __name__ == '__main__':
    main()
