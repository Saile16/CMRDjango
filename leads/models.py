from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User = get_user_model()


class User(AbstractUser):
    pass


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # Foreing key
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    # OneToOneField tgiene que ir relacionado a un foreingkey
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # estos 2 lo tenemos dentro de abstractUser
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email
