# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

MAKE_CHOICES = (
    ('audi','AUDI'),
    ('bmw', 'BMW'),
)


class Cars(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    date = models.DateField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    make = models.TextField(blank=True, null=True, choices=MAKE_CHOICES, default='audi')
    model = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    wd = models.TextField(blank=True, null=True)
    fuel = models.TextField(blank=True, null=True)
    comment_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'

    def __str__(self):
        return f'{self.make} - {self.model}'



