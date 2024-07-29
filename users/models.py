from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Painting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users_image/', blank=True, null=True, default='default_images/user_image.png')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'painting'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users_image/', default='default_images/user_image.png')

    def __str__(self):
        return f'{self.user.username} Profile'


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_message', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_message', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} at {self.timestamp}'









