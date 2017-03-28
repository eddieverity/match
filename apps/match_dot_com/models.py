from __future__ import unicode_literals

from django.db import models

class User(models.Model):
  first_name=models.CharField(max_length=64)
  last_name=models.CharField(max_length=64)
  email=models.CharField(max_length=64, unique=True)
  password=models.CharField(max_length=512)
  zipcode=models.IntegerField()

class Profile(models.Model):
  user=models.ForeignKey(User, related_name='user_profile')
  gender=models.CharField(max_length=64, blank=True, null=True)
  age=models.IntegerField(blank=True, null=True)
  height=models.IntegerField(blank=True, null=True)
  body=models.IntegerField(blank=True, null=True)
  relationship_status=models.CharField(max_length=64, blank=True, null=True)
  current_kids=models.IntegerField(blank=True, null=True)
  future_kids=models.IntegerField(blank=True, null=True)
  education=models.IntegerField(blank=True, null=True)
  smoke=models.IntegerField(blank=True, null=True)
  drink=models.IntegerField(blank=True, null=True)
  religion=models.CharField(max_length=64, blank=True, null=True)
  salary=models.IntegerField(blank=True, null=True)

#aggregates determined on a scale of 0-10 in views used for matchmaking
  activity=models.IntegerField()
  frugality=models.IntegerField()
  pragmaticism=models.IntegerField()
  family=models.IntegerField()

class Seeking(models.Model):
  user=models.ForeignKey(User, related_name='user_seeking') 
  gender=models.CharField(max_length=64, blank=True, null=True)
  age=models.IntegerField(blank=True, null=True)
  height=models.IntegerField(blank=True, null=True)
  body=models.IntegerField(blank=True, null=True)
  relationship_status=models.CharField(max_length=64, blank=True, null=True)
  current_kids=models.IntegerField(blank=True, null=True)
  future_kids=models.IntegerField(blank=True, null=True)
  education=models.IntegerField(blank=True, null=True)
  smoke=models.IntegerField(blank=True, null=True)
  drink=models.IntegerField(blank=True, null=True)
  religion=models.CharField(max_length=64, blank=True, null=True)
  salary=models.IntegerField(blank=True, null=True)

#aggregates determined on a scale of 0-10 in views used for matchmaking
  activity=models.IntegerField()
  frugality=models.IntegerField()
  pragmaticism=models.IntegerField()
  family=models.IntegerField()

class Images(models.Model):
  user=models.ForeignKey(User, related_name='user_pics')
  user_pic=models.ImageField(upload_to = 'pic/folder/', default='pic/folder/none/no-img.jpg')

class Messages(models.Model):
  sender=models.ForeignKey(User, related_name='user')
  recipient=models.ForeignKey(User, related_name='user_recipient')
  description=models.CharField(max_length=1024)

class Wink(models.Model):
  sender=models.ForeignKey(User, related_name='user_wink')
  recipient=models.ForeignKey(User, related_name='wink_recipient')
