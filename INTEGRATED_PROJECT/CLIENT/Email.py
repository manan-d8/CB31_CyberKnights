import smtplib, email, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
from datetime import datetime
import time
class alert_Handle:
    def __init__(self,DB):
        self.visitors = []
        self.db = DB

    def Sendmails(self):
        print(" Sendmails "*40)
        self.fetchVisitors()
        for x in self.visitors:
            print(x)
        self.run()
    # def DB_Connect(self):
    #     mydb = mysql.connector.connect( host="192.168.1.223",
    #                                         user="SIH",
    #                                         password="SIH2020",
    #                                         database="SIH2020"
    #                                 )
    #     print("[ DATA BASE ]",mydb)
    #     return mydb

    def run(self):
            emailsql = 'SELECT * FROM alert_msg'
            cursorMail = self.db.cursor()
            cursorMail.execute(emailsql)
            emailandname = cursorMail.fetchall()
            cursorMail.close()
            lis = []
            for data in emailandname:
                trys = 3
                while trys>0:
                    try:
                        print("sending Message")
                        self.SendMail(data)   #name,mobileno,mail,role
                        break
                    except:
                        trys-=1
                        continue


    def fetchVisitors(self):
            fetch = 'SELECT * from currentvisitors'
            cursorMail = self.db.cursor()
            cursorMail.execute(fetch)
            emailandname = cursorMail.fetchall()
            cursorMail.close()
            lis = []
            for data in emailandname:
                self.visitors.append(data)

    def SendMail(self,data):
        try:
            print("working on email To :", data[2])
            name = data[0]
            email = data[2]
            role =  data[3]
            lang = data[4]

            msg = MIMEMultipart()
            msg["Subject"] = "ASCV Visitor Update"
            msg["From"] = "Alert <{0}>".format(email)
            msg["To"] = email
            #================================

            s = smtplib.SMTP_SSL("smtp.gmail.com:465")
            s.login("tangov.2508@gmail.com","Tango@123")


            if lang == "ENGLISH":
                MailMsg1 = """<body style='background-color : #E76F51'><center><h1> This Message is from Autometic Vehicle Monitoring System. </h1></<center></body>\n"""
            elif lang == "HINDI":
                MailMsg1 = """<body style='background-color : #E76F51'><center><h1> यह मैसेज ऑटोमेटिक व्हीकल मॉनिटरिंग सिस्टम की और से है। </h1></<center></body>\n"""
            elif lang == "GUJARATI":
                MailMsg1 = """<body style='background-color : #E76F51'><center><h1> આ સંદેશ ઓટૉમેટીક વેહીકલ મોનીટરીંગ​ સીસટમ​ ની તરફ થી છે. </h1></<center></body>\n"""
            else:
                print("Somethings wrong")

            msg.attach(MIMEText(MailMsg1,"html"))
            if lang == "ENGLISH":
                Msglbl2 = """<div  style='background-color : #E9C46A'><center><h2>This visitors are currently available inside premises. </h2></<center></div>\n\n\n"""
            elif lang == "HINDI":
                Msglbl2 = """<div  style='background-color : #E9C46A'><center><h2>ये मुलाकाती अभी संस्था में मौजूद है।</h2></<center></div> \n\n\n"""
            elif lang == "GUJARATI":
                Msglbl2 = """<div  style='background-color : #E9C46A'><center><h2>આ મુલાકાતિઓ હજી સંસ્થા માં હાજીર​ છે.</h2></<center></div> \n\n\n""" 
            else:
                print("Somethings wrong")

            msg.attach(MIMEText(Msglbl2,"html"))

            if lang == "ENGLISH":
                str1= """
                <table style="width:100%">
                  <tr>
                    <th style="border: 2px solid black" ><h3>Vehicle NO </h3></th>
                    <th style="border: 2px solid black" ><h3>ENTERING TIME</h3></th>
                  </tr>
            """
            elif lang == "HINDI":
                str1= """
                <table style="width:100%">
                  <tr>
                    <th style="border: 2px solid black" ><h3> वाहन नंबर </h3></th>
                    <th style="border: 2px solid black" ><h3> अंदर आने का समय  </h3></th>
                  </tr>
                """
            elif lang == "GUJARATI":
                str1= """
                <table style="width:100%">
                  <tr>
                    <th style="border: 2px solid black" ><h3> વાહન નંબર​ </h3></th>
                    <th style="border: 2px solid black" ><h3> અંદર આવાનો સમય </h3></th>
                  </tr>
                """
            for d in self.visitors:
                str1 += """
                    <tr style="border: 2px solid black">
                        <td style="border: 2px solid black"><h3>{0}</h4></td>
                        <td style="border: 2px solid black"><h3>{1}</h4></td>
                    </tr>
                """.format(d[1],d[2])

            msg.attach(MIMEText(str1,"html"))
            s.sendmail("tangov.2508@gmail.com", email, msg.as_string())
            print("email sent")
        except Exception as e:
            print(e)
            raise Exception



if __name__ == '__main__':
    Db_H = alert_Handle()
    Db_H.Sendmails()
