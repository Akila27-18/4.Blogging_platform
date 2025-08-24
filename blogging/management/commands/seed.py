
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blogging.models import Category, Post, Comment
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import random

class Command(BaseCommand):
    help = "Seed database with sample users, categories, posts, and comments."

    def handle(self, *args, **options):
        # Users
        if not User.objects.filter(username='alice').exists():
            alice = User.objects.create_user('alice', password='pass12345', email='alice@example.com')
        else:
            alice = User.objects.get(username='alice')
        if not User.objects.filter(username='bob').exists():
            bob = User.objects.create_user('bob', password='pass12345', email='bob@example.com')
        else:
            bob = User.objects.get(username='bob')
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', email='admin@example.com', password='admin12345')
        else:
            admin = User.objects.get(username='admin')

        # Categories
        cats = ['Tech','Travel','Lifestyle','Food','Design']
        cat_objs = []
        for c in cats:
            obj, _ = Category.objects.get_or_create(name=c)
            cat_objs.append(obj)

        # Generate placeholder image
        def make_image(color=(200,200,200), size=(800,400), text='Blog Image'):
            img = Image.new('RGB', size, color)
            bio = BytesIO()
            img.save(bio, format='JPEG')
            return ContentFile(bio.getvalue(), 'placeholder.jpg')

        # Posts
        sample_posts = [
            ('Welcome to the Blogging Platform', 'This is a demo post showing how the platform works. You can create, edit, and delete posts, add comments, and more.'),
            ('10 Tips for Productive Coding', 'Consistency and small daily progress wins. Use version control, write tests, and keep your code clean.'),
            ('Exploring the Mountains', 'A short travel diary about hiking and the joy of reaching summits.'),
            ('Design Systems 101', 'How to think in components, tokens, and accessibility from day one.'),
            ('Best Coffee in Town', 'A tour of cozy spots with latte art and quiet corners to read.')
        ]
        for title, content in sample_posts:
            if not Post.objects.filter(title=title).exists():
                author = random.choice([alice, bob])
                p = Post.objects.create(title=title, content=content, author=author)
                p.image.save('placeholder.jpg', make_image(), save=True)
                p.categories.add(*random.sample(cat_objs, k=2))

        # Comments (unapproved and approved)
        for p in Post.objects.all():
            Comment.objects.get_or_create(post=p, user=alice, text="Great read! Thanks for sharing.", approved=True)
            Comment.objects.get_or_create(post=p, user=bob, text="I have a question about this.", approved=False)

        self.stdout.write(self.style.SUCCESS("Seed data created. Users: alice/bob (pass12345), admin (admin12345)"))
