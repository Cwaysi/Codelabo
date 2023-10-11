from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectRequest)
admin.site.register(Cofounders)
admin.site.register(TechStack)
admin.site.register(UserProfile)