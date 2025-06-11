from django.db import models

from apps.users.models import User


class Story(models.Model):
    STATUS_CHOICES = (
        ('user', "User"),
        ('doctor', "Doctor"),
        ('nurse', "Nurse")
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='stories/')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StoryView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')

