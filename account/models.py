from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        print("creating a superuser")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    # def create_user(self, email, password=None, **extra_fields):
    #     email = self.normalize_email(email)
    #     user = self.model(email=email)
    #     user.set_password(password)
    #     user.is_active = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        activation_code = str(uuid.uuid4())
        self.activation_code = activation_code


# class MyUserManager(BaseUserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("The given username must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.create_activation_code()
#         user.set_password(password)
#         user.save(using=self._db)
#         #
#         # if password:
#         #     user.set_password(password)
#         # user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_active', False)
#         extra_fields.setdefault('is_staff', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_active') is not True:
#             raise ValueError('is_active must be True')
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('is_staff must be True')
#         return self._create_user(email, password, **extra_fields)
#
#
# class MyUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     username = None
#     is_active = models.BooleanField(default=False)
#     activation_code = models.CharField(max_length=100, blank=True)
#     objects = MyUserManager()
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return f'{self.email}'


#TODO: create activation code


