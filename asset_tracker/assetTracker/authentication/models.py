from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom User manage.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_system_admin = models.BooleanField(default=True)
    remember_user = models.BooleanField(default=False)
    

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "is_system_admin"]

    def __str__(self):
        return self.email
    
    @classmethod
    def get_by_email(cls, email):
        user = None
        try:
            user = cls.objects.get(email=email)
        except Exception as exc:
            print("Exception occured in CustomUser.get_by_email as ", str(exc))
        return user
    
    @classmethod
    def update(cls, email, updated_values):
        user = cls.get_by_email(email=email)
        for key, value in updated_values.items():
            setattr(user, key, value)
        user.save()
        return user
