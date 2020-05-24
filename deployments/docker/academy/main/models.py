from django.conf import  settings
from email.message import EmailMessage
import smtplib



#generating the e-mail template 
class Emailer():
    email = getattr(settings, 'EMAIL_HOST_USER', None)
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)

    msg = EmailMessage()
    
    def send_email(self, email, txt_template=None):

        self.msg['Subject'] = 'Welcome to FuChiCorp!' 
        self.msg['From'] = 'settings.EMAIL_HOST_USER'
        self.msg['To'] = email

        if txt_template is None:
            self.msg.add_alternative("""\
                <html>
                    <head>
                    </head>
                    <body">
                    <center>
                        <h1 style="color: linear-gradient(to top, #a18cd1 0%, #fbc2eb 100%); font-weight: bold;"> Welcome To FuChiCorp-Pynote </h1>
                        <h5>Thank you for joing our newsletter </h5>
                        <h4>Check our website for more detials : <a style="color:blue;">https://academy.fuchicorp.com</a></h4>
                    </center>
                    </body>
                </html>
            """,subtype='html')

        else:
            self.msg.add_alternative(txt_template,subtype='html')
            
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:        
            smtp.login(self.email, self.password)
            smtp.send_message(self.msg)