import smtplib, email, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
from datetime import datetime
import time
class alert_Handle:
    def __init__(self):
        self.visitors = []
        self.db = self.DB_Connect()
        self.fetchVisitors()
        for x in self.visitors:
            print(x)
        self.run()

    def DB_Connect(self):
        mydb = mysql.connector.connect( host="192.168.1.223",
                                            user="SIH",
                                            password="SIH2020",
                                            database="SIH2020"
                                            )
        print("[ DATA BASE ]",mydb)
        return mydb

    def run(self):
            emailsql = 'SELECT * FROM alert_msg'
            cursorMail = self.db.cursor()
            cursorMail.execute(emailsql)
            emailandname = cursorMail.fetchall()
            cursorMail.close()
            lis = []
            # for data in emailandname:
            self.SendMail(emailandname[0])   #name,mobileno,mail,role

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
            print("working on owners email")
            name = data[0]
            email = data[2]

            msg = MIMEMultipart()
            msg["Subject"] = "ASCV Visitor Update"
            msg["From"] = "Alert <{0}>".format(email)
            msg["To"] = email
            #================================

            s = smtplib.SMTP_SSL("smtp.gmail.com:465")
            s.login("tangov.2508@gmail.com","Tango@123")

            MailMsg1 = "This Message is from Autometic Vehicle Monitoring System."  
            MailMsg2 = "यह मैसेज ऑटोमेटिक व्हीकल मॉनिटरिंग सिस्टम की और से है।"
            MailMsg3 = "આ સંદેશ ઓટૉમેટીક વેહીકલ  મોનીટરીંગ​ સીસટમ​ ની તરફ થી છે."
            MailMsg1 = MailMsg1+"\n"+MailMsg2+"\n"+MailMsg3
            
            msg.attach(MIMEText(MailMsg1,"plain"))

            Msglbl1 = "This visitors are currently available inside premises."
            Msglbl2 = "ये मुलाकाती अभी संस्था में मौजूद है।"
            Msglbl3 = "આ મુલાકાતિઓ હજી સંસ્થા માં હાજીર​ છે."
            MailMsg1 = Msglbl1+"\n"+Msglbl2+"\n"+Msglbl3

            msg.attach(MIMEText(MailMsg1,"plain"))
            str1= ''
            for d in self.visitors:
                str1=str1+"Vehicle NO : "+d[1]+" TIME : "+d[2]+'\n' 

            msg.attach(MIMEText(str1,"plain"))

            s.sendmail("tangov.2508@gmail.com", email, msg.as_string())
            print("email sent")
        except Exception as e:
            print("error")
            print(e)



if __name__ == '__main__':
    Db_H = alert_Handle()
