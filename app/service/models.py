from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.urls import reverse

# from location_field.models.plain import PlainLocationField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    is_service_provider = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class ServiceArea(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    service_area = models.ForeignKey(ServiceArea, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[(
        "Open", "Open"), ("In Progress", "In Progress"), ("Completed", "Completed")])
    
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.description[:20]


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    # contact_details = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to="company_logos/", null=True)
    company_description = models.TextField()
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    service_area = models.ManyToManyField(ServiceArea)
    service_type = models.ManyToManyField(ServiceType)
    # location = PlainLocationField(based_fields=['city'], zoom=7)
    email = models.EmailField()  # Add the email field
    
    def get_absolute_url(self):
        return reverse('service_provider_list')
    
    def __str__(self):
        return self.business_name


class PreviousWork(models.Model):
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="previous_work/")
    description = models.TextField()

    def __str__(self):
        return self.service_provider.business_name + ": work"


class Offer(models.Model):
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='previous_work')
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    completion_time = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[(
        "Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")])

    def __str__(self):
        return self.service_provider.business_name + ": offer : " + str(self.cost_estimate)


class ChatMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver_messages')
    service_request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + ": <-> : " + self.receiver.username
