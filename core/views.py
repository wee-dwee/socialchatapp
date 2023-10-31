from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from itertools import chain
import random
# Create your views here.

@login_required(login_url='signin')
def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.filter(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('home')

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    if request.method=='POST':
        username=request.POST.get('username',False)
        username_object=User.objects.filter(username__icontains=username)

        username_profile=[]
        username_profile_list=[]

        for i in username_object:
            username_profile.append(i.id)

        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list=list(chain(*username_profile_list))
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})


@login_required(login_url='signin')
def home(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile_object=Profile.objects.get(user=user_object)
    posts=post.objects.all()

    following_list=[]
    feed=[]

    user_following=FollowersCount.objects.filter(follower=request.user.username)

    for i in user_following:
        following_list.append(i)

    for i in following_list:
        feed_lists=post.objects.filter(user=i)
        feed.append(feed_lists)

    feed_list=list(chain(*feed))


    all_users=User.objects.all()
    user_following_all=[]

    for i in user_following:
        user_list=User.objects.get(username=i.user)
        user_following_all.append(user_list)

    user_suggestion_list=[x for x in list(all_users) if (x not in list(user_following_all))]

    me =User.objects.filter(username=request.user.username)

    suggestions=[x for x in list(user_suggestion_list) if (x not in list(me))]
    random.shuffle(suggestions)

    username_profile=[]
    username_profile_list=[]

    for i in suggestions:
        username_profile.append(i.id)

    for ids in username_profile:
        profile_lists=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_list=list(chain(*username_profile_list))
    return render(request,'index.html',{'user_profile':user_profile_object,'posts':posts,'feed_list':feed_list,'suggestions':suggestions_list[:4]})

@login_required(login_url='signin')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=post.objects.filter(user=pk)
    user_posts_len=len(user_posts)

    follower=request.user.username
    user=pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='Unfollow'
    else:
        button_text='follow'

    followers=len(FollowersCount.objects.filter(user=pk))
    following=len(FollowersCount.objects.filter(follower=pk))
    return render(request,'profile.html',{'user_object':user_object,'user_profile':user_profile,'user_posts': user_posts,'user_posts_len':user_posts_len,'button_text':button_text,'followers':followers,'following':following})

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method=="POST":
        if request.FILES.get('profile-image') == None:
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        else:
            image=request.FILES.get('profile-image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home')

@login_required(login_url='signin')
def likepost(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post_ins=post.objects.get(id=post_id)
    like_filter=like_post.objects.filter(post_id=post_id,username=username).first()

    if like_filter == None:
        new_like=like_post.objects.create(post_id=post_id,username=username)
        new_like.save()
        post_ins.no_of_likes=post_ins.no_of_likes+1
        post_ins.save()
        return redirect('home')
    
    else:
        like_filter.delete()
        post_ins.no_of_likes=post_ins.no_of_likes-1
        post_ins.save()
        return redirect('home')
    

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"E-mail already exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=pass1)
                user.save()
                user_login= user=auth.authenticate(username=username,password=pass1)
                
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signin')

        else:
            messages.info(request,"Passwords not matching")
            return redirect('signup')

    else:
        return render(request,'signup.html',{'messages':messages})
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        
        else:
            return redirect('signin')
    else:
        return render(request,'signin.html')
    
def logout(request):
    auth.logout(request)
    return redirect(signin)