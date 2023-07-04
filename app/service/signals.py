
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceRequest
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Offer


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            return
        try:
            offer = Offer.objects.get(pk=ipn_obj.invoice)
            assert ipn_obj.mc_gross == offer.cost_estimate and ipn_obj.mc_currency == 'USD'
        except Exception:
            print('Paypal ipn_obj data not valid!')
        else:
            print("paid--------")
            # offer.paid = True
            # offer.save()
    else:
        print('Paypal payment status not completed: %s' % ipn_obj.payment_status)



@receiver(post_save, sender=ServiceRequest)
def send_email_notification(sender, instance, created, **kwargs):
    if created and instance.client is None:
        subject = 'New Service Request without Client'
        html_content = render_to_string('service/email_template.html', {
            'full_name': instance.full_name,
            'address': instance.address,
            'phone_number': instance.phone_number,
            'service_area': instance.service_area,
            'service_type': instance.service_type,
            'description': instance.description,
        })
        text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.

        msg = EmailMultiAlternatives(
            subject, text_content, 'kamal.umar0987@gmail.com', ['kamal.umar0987@gmail.com']
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()