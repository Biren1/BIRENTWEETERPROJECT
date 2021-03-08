
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Tweet
from datetime import datetime
import os


# def home(request):
#     # data =Tweet.objects.all()
#     # comm ={}
#     # for k in data:
#     #     comm[k.id] = Tweet.objects.filter(parent_tweet_id=k.id).count()
#     #
#     # params = {'data': data, 'comm': comm}
#     return render(request,'home.html')
# def index(request):
#     return render(request,'index.html')
# def post_tweet(request):
#     return render(request, 'post-tweet.html')
# def tweet_detail(request):
#     return render(request, 'tweet-detail.html')

def home(request):
     #Helper function to get comment count
     def get_reply_count(tweetid):
         count = Tweet.objects.filter(parent_tweet_id=tweetid).count()
         return count
     all_tweets = Tweet.objects.all().order_by('-created_at')
     #Adding comment count for each tweet
     for tweet in all_tweets:
         count = get_reply_count(tweet.id)
         tweet.count = count
     all_tweets = Tweet.objects.all()
     context = {
        "all_tweets": all_tweets
    }
    # Render Page
     return render(request,'home.html', context)


def post_tweet(request):
    # if parent_tweet_id is not 0:
    #    replies=Tweet.objects.order_by('-created_at').filiter(parent_tweet_id=parent_tweet_id)
    #    context={
    #        "replies":replies,
    #        "parent_tweet_id":parent_tweet_id,
    #    }
    #    return render (request,'post-tweet.html',context)
    # else:
       return render(request, 'post-tweet.html')

def tweet_detail(request,parent_tweet_id):
    details=Tweet.objects.order_by('-created_at').filter(parent_tweet_id=parent_tweet_id)
    context={
        "details":details,
        "parent_tweet_id":parent_tweet_id
    }
    return render(request,'tweet-detail.html',context)


def process_form(request):
    fileitem = request.FILES.get('tweet-image', None)
    title = request.POST['name']
    text = request.POST.get('comment', False)
    dateTime = datetime.now()
    formtype = request.POST['formtype']
    # comment = request.POST.get('comment',False)


    #print(fileitem)
    # if title.strip() == '' or text.strip() == '':
    #      return render(request, '')
     #Test if the file was uploaded
    if fileitem:

           with open('tweets/static/userimage/' + str(fileitem), 'wb+') as destination:
                for chunk in fileitem.chunks():
                    destination.write(chunk)
           imageurl = '' \
                      'userimage/' + str(fileitem)
    else:
         imageurl = None
         usrmsg = 'No file was uploaded'

    new_tweet = Tweet(name=title,
                      text=text, image_path=imageurl, created_at=dateTime)
    new_tweet.save()

    return HttpResponseRedirect(reverse('home'))

def reply(request,parent_tweet_id):
    if request.POST:
        fileitem = request.FILES.get('tweet-image', None)
        title = request.POST['name']
        text = request.POST.get('comment', False)
        dateTime = datetime.now()
        formtype = request.POST['formtype']
        # comment = request.POST.get('comment',False)

        # print(fileitem)
        # if title.strip() == '' or text.strip() == '':
        #      return render(request, '')
        # Test if the file was uploaded
        if fileitem:

            with open('tweets/static/userimage/' + str(fileitem), 'wb+') as destination:
                for chunk in fileitem.chunks():
                    destination.write(chunk)
            imageurl = 'tweets/static/userimage/' + str(fileitem)
        else:
            imageurl = None
            usrmsg = 'No file was uploaded'
        new_tweet = Tweet(parent_tweet_id=parent_tweet_id, name=title,
                      text=text, image_path=imageurl, created_at=dateTime)
        new_tweet.save()
    return render(request, 'reply.html')
