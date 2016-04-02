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

def main():

# 01 ask for file name to read
  filename = raw_input("Enter the file name: ")
  if len(filename) < 3: filename = "meg_new.txt"
  csv_m = file_open(filename)
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
  for line_meg in csv_m:
    if "Минута" in line_meg or "Секунда" in line_meg:
      megafon = line_meg.split(";")
      if megafon[5]: phone_num = megafon[5]
      phone_num.split()
      try:
        operator = int(phone_num[:3])
        region = int(phone_num[3:])
        M = phone_num[0]
      except:
        True
#      print type(phone_num),operator,region

# 04 open rosstat csv file by direct phone number from megafon file
      try:
        ros_csv = csv[M]
#        print "File is open: M"
      except:
        ros_csv = False ЕСЛИ ФАЙЛА НУЖНОГО НЕТ ТО КАКОЙ ОПЕРАТОР И РЕГИОН?

# 02 read the string
      if ros_csv:
        for line in ros_csv:
          newline = line.split(';')
          #operator=921
        #print int(newline[0])
          try:
            ros_op = int(newline[0])
            ros_reg1 = int(newline[1])
            ros_reg2 = int(newline[2])
            if operator==ros_op and region>ros_reg1 and region<ros_reg2:
              print "Operator: ",operator, newline[4], "Region: ", region, newline[5]
          except:
            True ЕСЛИ В ФАЙЛЕ НЕТ НУЖНОГО СОВПАДЕНИЯ ТО КАКОЙ РЕГИОН И КАКОЙ ОПЕРАТОР


    '''newline = text.split(';')
    newline[0] = newline[0].strip()
    try:
      num = int(newline[0])
      print "##",num,type(num),"##"
    except:
      print "#",newline[0],type(newline[0]),"#"'''

# 02 read CSV_rosstat files:



# 09 coles files
  csv_m.close()

if __name__ == '__main__':
    main()
