from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and save new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Function to created superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Modalidade(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ativo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    modalidades = models.ManyToManyField('Modalidade', blank=False)

    def __str__(self):
        return self.name


class Aplicacao(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_solicitation = models.DateTimeField(auto_now_add=True)
    quantity = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    ativos = models.ManyToManyField('Ativo', blank=False)

    def __repr__(self):
        return self.value


class Resgate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_solicitation = models.DateTimeField(auto_now_add=True)
    quantity = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    ativos = models.ManyToManyField('Ativo', blank=False)

    def __repr__(self):
        return self.value
