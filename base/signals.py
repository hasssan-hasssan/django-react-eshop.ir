from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone



def updateUser(sender, instance, **kwargs):
    user = instance

    if user.email != "":
        user.username = user.email

    # print(f'{user.username} updated !  ;-)')


pre_save.connect(receiver=updateUser, sender=User)


# Get an instance of a logger
logger = logging.getLogger(__name__)
def newUserAlert(sender, instance, created, **kwargs):
    user = instance
    msg = f"New user just registered:\n|Email: {user.email}\n|Name: {user.first_name}\n|Date joined: {user.date_joined.strftime('%d-%m-%Y %H:%M:%S')}"
    if created:
        try:
            send_mail(
                'Yo Yo Yo, new user on eshop',
                msg,
                'eshop.hamruyesh@gmail.com',
                ['abolfazl.hassanzade.81@gmail.com',]
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")

post_save.connect(newUserAlert, sender=User)

        