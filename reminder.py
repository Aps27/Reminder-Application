'''
Application to create, update and view reminders based on date and month provided. To run mostly on a Linux system.
'''

import sys
import MySQLdb
import time 
import os 

def checkSchedule(): 
	cursor.execute("select * from reminders")
	try:
		result=cursor.fetchall()
		for row in result:
			r=row[0]
			n=row[1]
			m1=row[2]
		month = time.strftime('%m') 
		date = time.strftime('%d')
		flag = 0
		#print month,r,date,n
		if int(month)==r and int(date)==n:
			flag =1
			os.system('notify-send "Events for Today: ' + m1 + '"') 
		if flag == 0: 
			os.system('notify-send "No events scheduled today!"')  
	except:
			print "Display error, please try again..."
			
db=MySQLdb.connect("host","username","password","database_name")
cursor=db.cursor()
checkSchedule() # are there any reminders today?

try:
	cursor.execute("create table reminders(month int(5),date int(5), message varchar(30))")
	db.commit()
except:
	print "Could not create table..."
else:
	print "Table 'Reminders' successfully created..."
p=1
while p!=0:
	print "MENU"
	print "1.Add new reminder 2.Update a reminder 3.Display Reminders 4.Exit" 
	ch=input("Enter choice....")

	if ch == 1:
		try:
			m=input("Enter Month(MM): ")
			d=input("Enter Date(DD): ")
			msg=raw_input("Enter reminder message: ")
			cursor.execute("insert into reminders values('%d','%d','%s')"%(m,d,msg))		
			db.commit()
		except:
			print "Error in inserting values..."
		else:
			print "Successfully inserted value(s)..."	

	elif ch == 2:
		m=input("Enter month: ")
		d=input("Enter date: ")
		msg=raw_input("Enter updated reminder: ")
		cursor.execute("update reminders set message = '%s' where month='%d' and date='%d'"%(msg,m,d))
		db.commit()

	elif ch == 3:
		cursor.execute("select * from reminders")
		print "Month      Date       Reminders"
		print "---------------------------------"
		try:
			result=cursor.fetchall()
			for row in result:
				r=row[0]
				n=row[1]
				m1=row[2]
				print r,"         ",n,"       ",m1
		except:
			print "Display error"
	
	elif ch == 4:
		sys.exit()
	else:
		print "Enter valid option...."
	p=input("Do you want to continue?..")

checkSchedule() # check for reminders again
db.commit()
db.close()