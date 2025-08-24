
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment, Post

@receiver(post_save, sender=Comment)
def notify_on_new_comment(sender, instance, created, **kwargs):
    if created:
        subject = f"New comment on your post: {instance.post.title}"
        message = f"A new comment was added by {instance.user.username} on '{instance.post.title}'.\n\n{instance.text}"
        recipient_list = [instance.post.author.email] if instance.post.author.email else []
        if recipient_list:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

@receiver(post_save, sender=Post)
def alert_on_new_post(sender, instance, created, **kwargs):
    if created:
        subject = f"New blog post: {instance.title}"
        message = f"A new post has been published by {instance.author.username}: {instance.title}"
        # In a real app you would email subscribers. For demo, send to author if they have email.
        recipient_list = [instance.author.email] if instance.author.email else []
        if recipient_list:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
