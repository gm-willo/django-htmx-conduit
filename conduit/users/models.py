from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from config import settings


class CustomUserManager(UserManager):
    """custom UserManager with email as unique identifier instead of username"""

    def create_user(self, username, email, password=None):
        """Create and return a User with username, email and password"""

        if email is None:
            raise ValueError("Email is required.")
        if username is None:
            raise ValueError("Username is required.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        """Create and return a SuperUser with admin permissions"""

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    """Custom user model"""

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    # password field is already provided by AbstractUser

    USERNAME_FIELD = (
        "email"  # when a user logs in, he will enter his email in "username" field
    )
    REQUIRED_FIELDS = [
        "username"
    ]  # during sign up USERNAME_FIELD and password are mandatory by default

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile model associated to each User object"""

    # AUTH_USER_MODEL is a variable set in config/settings.py
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.URLField(
        default="https://static.productionready.io/images/smiley-cyrus.jpg"
    )
    bio = models.TextField(max_length=1000, blank=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    favorites = models.ManyToManyField(
        "articles.Article", related_name="favorited", blank=True
    )

    def follow(self, profile):
        """Follow `profile`"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile`"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Return True if `profile` is in self.follows, False otherwise"""
        return self.follows.filter(pk=profile.pk).exists()

    def favorite(self, article):
        """Add article to Favorites"""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Remove article from Favorites"""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Return True if article is in Favorite, False otherwise"""
        return self.favorites.filter(pk=article.pk).exists()

    def __str__(self):
        return self.user.username
