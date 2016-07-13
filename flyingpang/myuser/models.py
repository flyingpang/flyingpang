# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        Creates and saves a User with the given email, nickname, password.
        """
        if not nickname:
            raise ValueError('Users must have a nickname')

        if not email:
            raise ValueError('User must have a email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_supperuser(self, email, nickname, password):
        """
        Creates and saves a superuser with the given email, nickname, password.
        """
        user = self.create_user(
            email,
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    nickname = models.CharField(_(u'昵称'), max_length=40)
    email = models.EmailField()
    join_date = models.DateTimeField(_('加入日期'), auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyUserManager()

    REQUIRED_FIELDS = ['nickname',]

    def __unicode__(self):
        return self.nickname
