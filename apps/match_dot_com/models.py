from __future__ import unicode_literals
from django import forms
from django.db import models

class User(models.Model):
  first_name=models.CharField(max_length=64)
  last_name=models.CharField(max_length=64)
  email=models.CharField(max_length=64, unique=True)
  password=models.CharField(max_length=512)

  zipcode=models.IntegerField()

  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


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
  activity=models.IntegerField(blank=True, null=True)
  frugality=models.IntegerField(blank=True, null=True)
  pragmaticism=models.IntegerField(blank=True, null=True)
  family=models.IntegerField(blank=True, null=True)

class Seeking(models.Model):
  seeking_user=models.ForeignKey(User, related_name='user_seeking') 
  gender=models.CharField(max_length=64, blank=True, null=True)
  age_min=models.IntegerField(blank=True, null=True)
  age_max=models.IntegerField(blank=True, null=True)

  height_min=models.IntegerField(blank=True, null=True)
  height_max=models.IntegerField(blank=True, null=True)

  body=models.IntegerField(blank=True, null=True)
  deal_body=models.BooleanField(blank=True, null=False)

  relationship_status=models.IntegerField(blank=True, null=True)
  deal_relationship_status=models.BooleanField(blank=True, null=False)

  current_kids=models.IntegerField(blank=True, null=True)
  deal_current_kids=models.BooleanField(blank=True, null=False)

  future_kids=models.IntegerField(blank=True, null=True)
  deal_future_kids=models.BooleanField(blank=True, null=False)

  education=models.IntegerField(blank=True, null=True)
  deal_education=models.BooleanField(blank=True, null=False)

  smoke=models.IntegerField(blank=True, null=True)
  deal_smoke=models.BooleanField(blank=True, null=False)

  drink=models.IntegerField(blank=True, null=True)
  deal_drink=models.BooleanField(blank=True, null=False)

  religion=models.IntegerField(blank=True, null=True)
  deal_religion=models.BooleanField(blank=True, null=False)

  salary=models.IntegerField(blank=True, null=True)
  deal_salary=models.BooleanField(blank=True, null=False)

#aggregates determined on a scale of 0-10 in views used for matchmaking


class Images(models.Model):
  user=models.ForeignKey(User, related_name='user_pics')
  user_pic=models.FileField(upload_to = 'img')
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Messages(models.Model):
  sender=models.ForeignKey(User, related_name='user')
  recipient=models.ForeignKey(User, related_name='user_recipient')
  description=models.CharField(max_length=1024)
  message_read=models.NullBooleanField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Wink(models.Model):
  sender=models.ForeignKey(User, related_name='user_wink')
  recipient=models.ForeignKey(User, related_name='wink_recipient')
  wink_seen=models.NullBooleanField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
