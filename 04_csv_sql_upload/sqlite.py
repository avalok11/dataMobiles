#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


def main():

  conn = sqlite3.connect('../meg_call.db')
  sq = conn.cursor()

# 01 open CSV file
  csv_data = raw_input("Enter CSV data file name:")
  if len(csv_data)<1: csv_data = "meg_new_mod.txt"

# 02 read CSV data from file
  data = open(csv_data)

# 03 read all line in CSVs
  for item in data:
    item=item.split(";")
# for destionations table
    phone_num = item[5]
    digits3 = phone_num
    digits3.split()
    operator = item[4].decode('utf-8')
    region = item[7]
    if region=="Мурманская обл.":region="Мурманская область"
    region=region.decode('utf-8')
# for region table
    location = item[10].decode('utf-8')
    rouming = item[8]
# print rouming
    if rouming=="Минута": rouming="Home"
    else:
      rouming="Rouming"
# for users table
    user = item[1]
#for service
    service = item[9].decode('utf-8')
# for CALLs
    ddate = item[0]
    ttime = item[3]
    mminutes = item[6]
    ccost = item[11]

    #test
    #'''phone_num ="9219560459"
    #digits3="921"
    #region="StP"'''


# 04 put data to SQL
    sq.execute("INSERT OR IGNORE INTO directions_ (phone_num, digits3, operator, region) VALUES (?,?,?,?)",(phone_num,digits3[0:3],operator,region))
    sq.execute("INSERT OR IGNORE INTO region_ (location, region) VALUES (?,?)",(location,rouming))
    sq.execute("INSERT OR IGNORE INTO users_ (phone_number) VALUES (?)",(user,))
    sq.execute("INSERT OR IGNORE INTO service_ (servicetype) VALUES (?)", (service, ))

    direction_id = sq.execute("SELECT id FROM directions_ WHERE phone_num=?",(phone_num,))
    direction_id = direction_id.fetchone()[0]
    region_id = sq.execute("SELECT id FROM region_ WHERE location=? AND region=?",(location,rouming,))
    region_id = region_id.fetchone()[0]
    service_id = sq.execute("SELECT id FROM service_ WHERE servicetype=?",(service,))
    service_id = service_id.fetchone()[0]
    user_id = sq.execute("SELECT id FROM users_ WHERE phone_number=?",(user,))
    user_id = user_id.fetchone()[0]

    sq.execute("INSERT OR IGNORE INTO call_ (users_id,directions_id, services_id, region_id, date, time, minutes, cost) VALUES (?,?,?,?,?,?,?,?)", (user_id,direction_id,service_id,region_id,ddate,ttime,mminutes,ccost))

   # print region_id

#    c.execute("SELECT id FROM User WHERE name = ?",(user_name,))
#    user_id = c.fetchone()[0]
#    print user_id
#
#    c.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)",(title_course,))
#    c.execute("SELECT id FROM Course WHERE title = ?",(title_course,))
#    course_id = c.fetchone()[0]
#    print course_id
#    c.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES ( ?, ?, ? )''', ( user_id, course_id, role ) )

  conn.commit()

  conn.close()
  data.close()

if __name__ == '__main__':
    main()
