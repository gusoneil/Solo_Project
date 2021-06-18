from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        #First/Last name are long enough
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name must be more than 3 characters long'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last name must be more than 3 characters long'

        #Email is in correct format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):
            errors['email'] = 'must be a valid email'

        #Unique Email
        current_users = User.objects.filter(email = postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = 'Email is already in use'

        #Password
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if postData['password'] != postData['conf_pw']:
            errors['mismatch'] = 'Passwords must match'
        
        return errors

    def login_validator(self, postData):
        errors = {}
        
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif bcrypt.checkpw(postData['password'].encode(),existing_user[0].password.encode()) != True:
            errors['password'] = "Email and Password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['title']) < 3:
            errors['title'] = "Title needs to be at least 3 characters"
        if len(postData['title']) == 0:
            errors["title"] = "Title Field Required"
        if len(postData['year_released']) == 0:
            errors["year_released"] = "Year Released Field Required"
        if len(postData['developer']) < 3:
            errors['developer'] = 'Developed By needs to be a least 3 characters'
        if len(postData['developer']) == 0:
            errors['developer'] = 'Developed By Required'
        if len(postData['rating']) == 0:
            errors['rating'] = 'Rating Required'
        if len(postData['desc']) < 10:
            errors["desc"] = "Description needs to be at least 10 characters"
        if len(postData['desc']) == 0:
            errors["desc"] = "Description Field Required"
        return errors

class Review(models.Model):
    title = models.CharField(max_length=255)
    year_released = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    rating = models.IntegerField()
    desc = models.TextField()
    owner = models.ForeignKey(User, related_name='created_show', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = ReviewManager()
