from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowerCount
from .form import PostForm
from itertools import chain
import random
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_list = FollowerCount.objects.filter(follower=request.user.username).values_list('user', flat=True)
    
    feed_list = Post.objects.filter(user__in=user_following_list)
    
    all_users = User.objects.exclude(username=request.user.username)
    
    user_following_all = User.objects.filter(username__in=user_following_list)
    
    new_suggestion_list = all_users.exclude(username__in=user_following_all)
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = new_suggestion_list.exclude(username__in=user_following_list)
    
    final_suggestion_list = list(final_suggestion_list)
    random.shuffle(final_suggestion_list)
    
    suggestion_username_profile_list = Profile.objects.filter(user__in=final_suggestion_list)[:4]
    
    context = {
        'user_profile': user_profile, 
        'posts': feed_list,
        'suggestion_username_profile_list': suggestion_username_profile_list
    }
    
    return render(request, 'index.html', context)


@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=user_object)
    user_post_length = len(user_post)
    
    follower=request.user.username
    user=pk
    if FollowerCount.objects.filter(follower=follower,user=user).first():
        button_text="Unfollow"
    else:
        button_text="follow"
        
    user_follower=len(FollowerCount.objects.filter(user=pk))
    user_following=len(FollowerCount.objects.filter(follower=pk))
    context={
        "user_profile":user_profile,
        "user_object":user_object,
        "user_post":user_post,
        "user_post_length":user_post_length,
        "button_text":button_text,
        "user_follower":user_follower,
        "user_following":user_following,
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method == 'POST':
        username = request.POST['username']
        username_objects = User.objects.filter(username__icontains=username)
        
        username_profile_list = []
        
        for user in username_objects:
            profile_lists = Profile.objects.filter(user=user)
            username_profile_list.extend(profile_lists)
        
        
    context = {
        "user_profile": user_profile,
        "username_profile_list": username_profile_list,
    }
    return render(request, 'search.html', context)


@login_required(login_url='signin')
def follower(request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['user']
        
        if FollowerCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowerCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=FollowerCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None: 
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_like=post.no_of_like+1
        post.save()
        return redirect('/')
    else:
        LikePost.objects.filter(post_id=post_id, username=username).delete()
        post.no_of_like=post.no_of_like-1
        post.save()
        return redirect('/')

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email is taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request,"password not match")
            return redirect('signup')
    else:
        return render(request,'signup.html')

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user=request.user.username
        image=request.FILES.get('image')
        caption=request.POST['caption']
        new_post=Post.objects.create(user=user,caption=caption,image=image)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if 'image' in request.FILES:  # Check if a new image is provided
            image = request.FILES['image']
            user_profile.Profile_img = image  # Use the correct attribute name
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('setting')

    return render(request, 'setting.html',{'user_profile':user_profile})

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:  # Check if the user is active
                auth.login(request, user)
                return redirect('index')  # Redirect to the 'index' page
            else:
                messages.error(request, 'Your account is not active.')
                return redirect('signin')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'signin.html')
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')