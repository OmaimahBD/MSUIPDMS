from django.db import models
from django.contrib.auth.models import AbstractUser


class User (AbstractUser):
    
    is_coordinator=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)
    profile = models.ImageField(null=True, default="profile-default.svg")
    id_number = models.CharField(max_length=50, null=True)
    college=models.ForeignKey('College',on_delete=models.SET_NULL, null=True)
    department=models.ForeignKey('Department',on_delete=models.SET_NULL, null=True)
    
   
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
  
  
    
   
    
    def __str__(self):
        return self.user.username


class Coordinator(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
 
      

    def __str__(self):
        return self.user.username
    


class College(models.Model):
    name=models.CharField(max_length=150)
  
    

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name=models.CharField(max_length=150)
    college=models.ForeignKey('College',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Type(models.Model):
    type=models.CharField(max_length=150,null=True)
    
    def __str__(self):
        return self.type

class SubType(models.Model):
    name=models.CharField(max_length=150)
    type=models.ForeignKey('Type',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class IntellectualProperty(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_intellectual_property')
    approvedBy = models.CharField(max_length=100, blank=True, null=True) 
    college=models.ForeignKey(College,on_delete=models.SET_NULL, null=True)
    department=models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    type=models.ForeignKey(Type,on_delete=models.SET_NULL, null=True)
    subtype=models.ForeignKey(SubType,on_delete=models.SET_NULL, null=True)
    created=models.DateTimeField(auto_now_add=True)
    approvedDate=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    disapprovedDate=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated=models.DateTimeField(auto_now=True)
    tittle = models.CharField(unique=False,max_length=100)
    description = models.TextField(max_length=100)
    file =models.FileField(upload_to='ResearchFile/')
    doc_text_tokens = models.TextField(blank=True, default='')
    cover =models.ImageField(null=True,blank=True,upload_to='cover/', default="Abtract Cover.svg")
    year=models.DateField(null=True)
    author = models.ManyToManyField(User, related_name='authored_intellectual_property') 
    mainauthor= models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='mainauthorfirstname_intellectual_property') 
    is_approved = models.BooleanField(default=False)
    is_pending= models.BooleanField(default=True)
    ipviews=models.IntegerField(default=0, null=True, blank=True)

  
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.tittle
    


class IPSimilarityScore(models.Model):
    doc_source = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE, related_name='similar_doc_source')
    doc_target = models.ForeignKey(IntellectualProperty, on_delete=models.CASCADE, related_name='similar_doc_target')
    score = models.FloatField(default=0)
    remarks = models.CharField(max_length=120, default='')
    timestamp = models.DateField(auto_now_add=True)

    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    intellectualproperty= models.ForeignKey(IntellectualProperty, on_delete=models.SET_NULL,null=True)
    content = models.TextField(max_length=500)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[0:50]
    
class CommenReply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment= models.ForeignKey(Comment, on_delete=models.SET_NULL,null=True)
    content = models.TextField(max_length=500)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[0:50]