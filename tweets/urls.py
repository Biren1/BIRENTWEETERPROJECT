from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [

    path('',views.home, name='home'),
    path('post-tweet/',views.post_tweet, name='post-tweet'),
    path('tweet_detail/<int:parent_tweet_id>',views.tweet_detail, name='tweet_detail'),
    path('process_form/',views.process_form, name='process_form'),
    path('reply/<int:parent_tweet_id>',views.reply, name='reply'),
    ]