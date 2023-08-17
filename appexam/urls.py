from django.urls import path
from . import views

urlpatterns = [
    path('Blogusersignup', views.Blogusersignup.as_view()),
    path('Bloguserlogin', views.Blogusersignup.as_view()),
    path('Createpost', views.Createpost.as_view()),
    path('Readpost', views.ReadPosts.as_view()),
    path('Updatepost', views.Updatepost.as_view()),
    path('Deletepost', views.DeletePost.as_view()),
]

