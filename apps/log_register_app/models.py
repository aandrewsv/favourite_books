from django.db import models
from datetime import *
import re

# Create your models here.
class UserManager(models.Manager):
    def validations(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname'] = "First name must be at least 2 characters long!"
        if len(postData['lname']) < 2: 
            errors['lname'] = "Last name must be at least 2 characters long!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if self.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long!"
        if postData['confirmpassword'] != postData['password']:
            errors['password'] = "Passwords doesn't match!"
        if postData['birthday_date'] == '':
            errors['birthday_date'] = "Birthday date input is empty!"
        elif datetime.strptime(postData['birthday_date'], "%Y-%m-%d") > datetime.now():
            errors['birthday_date'] = "Birthday date must be in the past!"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=60)
    lname = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    birthday_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()