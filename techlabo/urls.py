from django.urls import path, include
from . import views

#Urls views maping
urlpatterns = [
    path("", views.login_view, name='login'),
    path("logout", views.logout_view, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("home", views.home, name='home'),
    path("posted", views.posted, name='posted'),
    path("profile/complete", views.usercomp, name='usercomp'),
    path("posted/delete/<int:id>", views.deleteproject, name='deleteproject'),
    path("posted/edit/<int:id>", views.editproject, name='editproject'),
    path("profile/edit/<int:id>", views.editprofile, name='editprofile'),
    path("project/request/<int:id>", views.request, name='request'),
    path("founder/profile/<int:id>", views.fprofile, name='fprofile'),
    path("request/received", views.requestreceive, name='requestreceive'),
    path("request/accept/<int:id>", views.accept, name='accept'),
    path("request/withdraw/<int:id>", views.withdraw, name='withdraw'),
    path("cofounding", views.cofounding, name='cofounding'),
    path("messages", views.messag, name='messages'),
]