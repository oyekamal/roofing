
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceRequest
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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