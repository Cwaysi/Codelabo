from django.db import models
from django.contrib.auth.models import User, AbstractUser

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tech_stack = models.ManyToManyField('TechStack', null = True, blank=True)
    github = models.URLField(blank=True, null = True)
    linkedin = models.URLField(blank=True, null = True)
    phone = models.CharField(max_length=15,null = True, blank=True)
    location = models.CharField(max_length=100,null = True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)  # Date when the profile was created
    date_updated = models.DateTimeField(auto_now=True)      # Date when the profile was last updated
    def __str__(self):
        return str(self.user.first_name)
    
    
# Tech Stack Model
class TechStack(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Project Model
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField('Brief Description')
    industry = models.CharField(max_length=50)
    tech_stack_needed = models.ManyToManyField('TechStack')
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    cofounders_needed = models.PositiveIntegerField('Number of CoFounders needed')
    #is_visible = models.BooleanField(default=False)  # Project is not visible until approved
    date_created = models.DateTimeField(auto_now_add=True)  # Date when the project was created
    date_updated = models.DateTimeField(auto_now=True)      # Date when the project was last updated

    def __str__(self):
        return self.title
    
#cofounders model
class Cofounders(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    co_founders = models.ManyToManyField(User)
    def __str__(self):
        return str(self.project.title)
    
    
# Project Request Model
class ProjectRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)  # Date when the request was created
    date_updated = models.DateTimeField(auto_now=True)      # Date when the request was last updated

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
