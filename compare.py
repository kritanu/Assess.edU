from twilio.rest import Client
#Twilio credentials
account_sid = 'ACb21a4e30edb702c90c7480790cfe6ac1'
auth_token = 'e687f3dcba0a7d3041c01b2962f77653'
client = Client(account_sid, auth_token)
def twilio_sendsms(name, marks, mob_num):
	
	new_num = '+'+ str(mob_num)
	print(new_num)
	message = client.messages \
                .create(
                     body="Your ward {} scored {} out of {} at the {} exam on {}.".format( name, marks, no_q, subject, d2),
                     from_='+12565008525',
                     to=new_num
                 )
	print(message.sid)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import ast
import xlwt
from xlwt import Workbook 

from datetime import date
#Today's date
today = date.today()
d2 = today.strftime("%B %d, %Y")


# Firebase credentials for retrieving JSON
cred = credentials.Certificate('D:/Downloads/s2kgrader-firebase-adminsdk-a9mh4-7b9804a557.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://s2kgrader.firebaseio.com/'})


#Parse Data
ref = db.reference('Marks')
ref_qno = db.reference('TotalQuestion')

#Parsed JSON Format
json_db = ref.get()
json_db_qno = ref_qno.get()


#Convert JSON to Dict
data_dict = ast.literal_eval((str(json_db)))
#print(data_dict)
#NEED TO BE FIXED
# subject = "English"
# no_q = 10

def grader_addexcel( s_key, a_key, no_q, subject):
	ans_q = no_q
	marks = 0
	
	for i in range(no_q):
		pointer = (i+1)
		s_res = s_key.find(str(pointer))
		a_res = a_key.find(str(pointer))
		try:
			if(i<9):
				s_key_option = s_key[s_res+1]
			else:
				s_key_option = s_key[s_res+2]
		except IndexError:
			s_key_option = 0
		if(i<9):	
			a_key_option = a_key[a_res+1]
		else:
			a_key_option = a_key[a_res+2]
		if(s_key_option == a_key_option):
			marks+=1

	#finalmarks
	#Setup client and send message
	twilio_sendsms(str(obj["name"]), marks, obj["phoneno"])
	print(obj["name"], marks)
	sheet1.write(student_no, 0, obj["name"])
	sheet1.write(student_no, 1, obj["rollno"])
	sheet1.write(student_no, 2, "+"+str(obj["phoneno"]))
	sheet1.write(student_no, 3, marks)
	results_excel.save('results.xls')



results_excel = Workbook() 

for subs in json_db:
	student_no = -1
	subject = str(subs)
	print(subject)
	sheet1 = results_excel.add_sheet(subject)
	sheet1.write(0, 0, 'Name')
	sheet1.write(0, 1, 'Roll Number')
	sheet1.write(0, 2, 'Phone Number')
	sheet1.write(0, 3, 'Marks')
	no_q = int(json_db_qno[subject])
	print(no_q)
	for obj in data_dict[subject]:
		student_no += 1
		if(obj["name"] == "Teacher"):
			a_key = obj["answer"].replace(" ", "")
			a_key = a_key.upper()
		else:
			s_key = obj["answer"].replace(" ", "")
			s_key = s_key.upper()
			grader_addexcel(s_key, a_key, no_q, subject)

