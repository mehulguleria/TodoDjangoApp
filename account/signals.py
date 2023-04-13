from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings

from account.models import User

def sendregistrationmail(subject,message,tomail):
    mail = send_mail(subject,message,from_email=settings.EMAIL_HOST_USER,recipient_list=(tomail,),fail_silently=True)
    return mail


@receiver(post_save,sender=User)
def SendVerificationMail(sender,instance=None,created=False,**kwargs):
    if created:
        subject = "Registration Completed"
        message = "Thankyou for registration at our web site. Please user the code to verify your mail. Code: "+str(instance.verify)
        tomail = instance
        
        sendregistrationmail(subject,message,tomail)