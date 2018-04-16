from django.db import models
from django.core.validators import RegexValidator

from .validators import validate_file_extension, validate_phone, validate_email


class Contacts(models.Model):
    """ Contacts """
    name = models.CharField('Name',max_length=255, blank=False)
    company = models.CharField('Company',max_length=255, blank=False)
    email = models.EmailField('Email', validators=[validate_email], blank=False)
    phone = models.CharField('Phone', validators=[validate_phone], max_length=17,
                             blank=True) # validators should be a list
    interest = models.CharField('Interest', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Contacts'
        verbose_name_plural = 'Contacts'
        ordering = ['-name']
        unique_together = ('name', 'company', 'email', 'phone', 'interest')


class Import(models.Model):
    myfile = models.FileField("Choose file",
                              validators = [validate_file_extension])

