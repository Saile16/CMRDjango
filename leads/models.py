from django.db import models
#
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

# User = get_user_model()


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

# para que cada usuario tenga asignados sus agentes y solo lo que el agrego a su vista tenemos
# que crear un userprofile que ira ligado al user


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # Foreing key
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    # OneToOneField tgiene que ir relacionado a un foreingkey
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # estos 2 lo tenemos dentro de abstractUser
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email


# esta funcion junto con post_save van de la mano, SOLO cuando un usuario es CREADO
# se creara un UserProfile
def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
