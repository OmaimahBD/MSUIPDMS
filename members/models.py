from django.db import models

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname  = models.CharField(max_length = 255)
    phone     = models.IntegerField(null=True)
    email     = models.EmailField(null=True)
    
    def __str__(self) -> str:
        return f"{self.firstname }{" "} {self.lastname}"


   
class IntellectualProperty(models.Model):
    intId      = models.IntegerField(null=True)
    accountId  = models.IntegerField(null=True)
    intTittle  = models.CharField(max_length = 255)
    intDescrip = models.CharField(max_length = 255) 
    intFileUploaded = models.CharField(max_length = 255)
    intDate    = models.DateField(null=True)
    intTime    = models.DateTimeField(null=True)
    intType    = models.CharField(max_length = 255)
    intAuthor  = models.CharField(max_length = 255)
    
class Search(models.Model):
    searchId  = models.CharField(max_length = 255)
    intId      = models.IntegerField(null=True)
    searchId  = models.CharField(max_length = 255)


class ApprovedIP(models.Model):
    approvedId   = models.IntegerField(null=True)
    accountId    = models.IntegerField(null=True)
    commentId    = models.IntegerField(null=True)
    appDate      = models.DateField(null=True)
    appTime      = models.DateTimeField(null=True)
    appStatus    = models.BooleanField(null=False)

class Account(models.Model):
    accountId  = models.IntegerField(null=True)
    personId  = models.IntegerField(null=True)
    departmentId  = models.IntegerField(null=True)
    formId      = models.IntegerField(null=True)
    accountType    = models.CharField(max_length = 255)
    accountUsername  = models.CharField(max_length = 255)
    accountPassword = models.CharField(max_length = 255)
    accountStatus    = models.BooleanField(null=False)

class Comment(models.Model):
    commentId    = models.IntegerField(null=True)
    accountId    = models.IntegerField(null=True)
    commentContent   = models.CharField(max_length = 255)
    commentDate      = models.DateField(null=True)
    commentTime      = models.DateTimeField(null=True)
    commentStatus    = models.BooleanField(null=False)

class Forms(models.Model):
    formId    = models.IntegerField(null=True)
    CDA   = models.CharField(max_length = 255)
    NDA   = models.CharField(max_length = 255)

class Department(models.Model):
    departmentId    = models.IntegerField(null=True)
    collegeId       = models.IntegerField(null=True)
    deparmentName   = models.CharField(max_length = 255)
    departmentLogo  = models.ImageField(null=True)

class College(models.Model):
    collegeId       = models.IntegerField(null=True)
    collegeLogo     = models.ImageField(null=True)
    collegeAddress  = models.CharField(max_length = 255)
    collegeName     = models.CharField(max_length = 255)

class Person(models.Model):
    personId  = models.IntegerField(null=True)
    personFName     = models.CharField(max_length = 255)
    personLName     = models.CharField(max_length = 255)
    personMInitial  = models.CharField(max_length = 255)
    personGender    = models.BooleanField(null=False)
    personBirthdate = models.DateField(null=True)
    personAddress  = models.CharField(max_length = 255)
    personDegree  = models.IntegerField(null=True)
    personEmail    = models.CharField(max_length = 255)
    personNumber  = models.CharField(max_length = 255)

class Admin(models.Model):
    adminId    = models.IntegerField(null=True)
    personId    = models.IntegerField(null=True)
    adminIdNum   = models.CharField(max_length = 255)
    
   