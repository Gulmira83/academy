from django.conf import  settings
from email.message import EmailMessage
import smtplib

from django.db import models
from django.contrib.auth.models import User
from accounting.models import Plans
from django.db.models.signals import post_save
from django.dispatch import receiver

class Feature(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    feature_type= models.CharField(max_length=60,null=True)
    payment_confirmation = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last update',auto_now_add=True)
    
    def __str__(self):
         return  self.user.username




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