from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username


class KycModel(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE,related_name="profile")
    p_address = models.FileField(upload_to=user_directory_path, blank=True)
    curr_address = models.FileField(upload_to=user_directory_path, blank=True)
    primary_contact = models.CharField(max_length=10, blank=True)
    secondary_contact = models.CharField(max_length=10, blank=True)
    Address_choice = [
        ('p','Permanent Address'),
        ('c','Current Address'),
    ]
    delivery_address = models.CharField(max_length=1, choices=Address_choice, default='p')
    kyc_choice = [
        ('y','Verified'),
        ('n','Not Verified'),
    ]
    kyc_verified = models.CharField(max_length=1, choices=kyc_choice, default='n')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         KycModel.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender='auth.User')
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = KycModel(user=instance)
        profile.save()
