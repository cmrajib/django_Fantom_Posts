from PIL import Image
from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

# A user has one profile. That's why it is OneToOneField
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    birth_day = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=100,blank=True)
    image = models.ImageField(blank=True, null=True, default='users/noimage.png',upload_to='users/')
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)


#If image is bigger than it will resize
        img = Image.open(self.image.path)
        if img.height> 200 or img.width > 200:
            new_size = (200,200)
            img.thumbnail(new_size)
            img.save(self.image.path)


    def __str__(self):
        return self.user.username


# When a new user is registered, his profile will also be created automatically.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile,sender=settings.AUTH_USER_MODEL)
