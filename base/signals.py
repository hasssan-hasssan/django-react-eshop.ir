import logging,time
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone


@receiver(pre_save, sender=User)
def updateUser(sender, instance, **kwargs):
    user = instance

    if user.email != "":
        user.username = user.email

    # print(f'{user.username} updated !  ;-)')



# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def newUserAlert(sender, instance, created, **kwargs):
    user = instance
    e = len(f'Email: f{user.email}') * '-'
    n = len(f'Name : f{user.first_name}') * '-'
    d = len(f"Date joined: {user.date_joined.strftime('%d-%m-%Y %H:%M:%S')}") * '-'
    msg = f"""

    New user just registered:

    {e}
    | Email: {user.email} |
    {n}
    | Name: {user.first_name} |
    {d}
    | Date joined: {user.date_joined.strftime('%d-%m-%Y %H:%M:%S')} |
    """
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


order_created = Signal()

@receiver(order_created)
def newOrderAlert(sender, **kwargs):
    order = kwargs.get('order')
    user = kwargs.get('user')
    orderItems = order.orderitem_set.all()
    itemsPrice = sum(item.qty * item.price for item in orderItems)

    msg = f"""\n
    New order for user: {user.username}

    Order: #{order._id}
    -------------------

    OrderItems:
    """
    for item in orderItems:
        msg += f"""
        Name : {item.name}
        Qty : {item.qty}
        Price: {item.price}
        --------------------------
        """

    msg += f"\nTotal of items price: {itemsPrice}"
    msg += "\n---------------------------------------"

    try:
        send_mail(
            'New Order on E-Shop',
            msg,
            'eshop.hamruyesh@gmail.com',
            ['abolfazl.hassanzade.81@gmail.com']
        )
    except Exception as e:
        logger.error(f"Error sending email: {e}")
