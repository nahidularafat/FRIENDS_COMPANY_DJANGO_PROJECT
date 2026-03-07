# file path: protfolio/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Main Content Models ---

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome class, e.g., 'fas fa-laptop-code'")
    image = models.ImageField(upload_to='service_images/', blank=True, null=True, help_text="Optional image for the service")

    def __str__(self):
        return self.title
class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Developer(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    image = models.ImageField(upload_to='developers/')
    bio = models.TextField()
    cv_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

# --- নতুন Client মডেল ---
class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='client_logos/')
    website_url = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers are displayed first")

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name

# --- Review Model ---

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"

# --- User Profile Model ---

class Profile(models.Model):
    ROLE_CHOICES = (
        ('SUPERADMIN', 'Superadmin'),
        ('CLIENT', 'Client'),
        ('VISITOR', 'Visitor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VISITOR')

    def __str__(self):
        return f"{self.user.username}'s Profile - {self.role}"

# Signal to create a profile automatically when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='CLIENT') # Default role is Client

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()