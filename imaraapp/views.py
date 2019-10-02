from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime as dt
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import ScriptForm,UpdateForm,PostForm, ScriptForm, SponsorSignUpForm,ResourceForm,GroupForm, MemberForm, CreatorSignUpForm, SponsorSignUpForm
from .models import Script, SponsorProfile, Profile,Projects, Profile, Resource, Group, Members, Projects,Creator,Members,CreatorProfile,Room, Category, CurriculumCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login, authenticate, logout as dj_logout
from .google import get_video_stats
from urllib.parse import urlparse, parse_qs
import requests
from django.contrib.auth import login as login, authenticate, logout as logout
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
import json
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from .serializers import CreatorSerializer
from rest_framework import status
 
from rest_framework.decorators import api_view
 
from rest_framework.response import Response
 
from .models import Creator
 





User = get_user_model()



# Create your views here.

@api_view(['GET','POST'])
def creator_list(request):
 
 
    if request.method == 'GET':
    
        creators = Creator.objects.all()
        
        serializer = CreatorSerializer(creators, many=True)
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
    
        serializer = creatorSerializer(data=request.data)
    
    if serializer.is_valid():
    
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    print(request.user)
    return render(request, 'home.html')

def chat(request):
    return render(request, 'room.html', {})


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]



def roomm(request, room_name):
    return render(request, 'roomm.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })

def all_rooms(request):
    room = Room.objects.all()
    return render(request, 'rooms.html', {'room':room})

def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'room_detail.html', {'room':room})
 

def sponsorsignup(request):     
    if request.method == 'POST':
        form = SponsorSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_sponsor = True
            user.save()
            sponsor = SponsorProfile.objects.create(user=user,first_name = form.cleaned_data.get('first_name'),  last_name = form.cleaned_data.get('last_name'),  email = form.cleaned_data.get('email'),  address = form.cleaned_data.get('address'),  organization = form.cleaned_data.get('organization'),  phone = form.cleaned_data.get('phone') ) 
            sponsor.refresh_from_db()
            sponsor.save()
            print(request.POST.get('location'))
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
        return redirect('login')

    else:
        form = SponsorSignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})



def sponsorlogin(request):
    if request.POST.get('username') and request.POST.get("password"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('hello from login')
            login(request, user)
            if user.is_sponsor == True:
                return redirect('sponsor')
            else:
                return render(request, 'registration/registration_form.html', {'form': form})
        else:
            print('user is none')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get  ('HTTP_REFERER'))




def creatorsignup(request):
    if request.method == 'POST':
        form = CreatorSignUpForm(request.POST)
        print(form)
        if form.is_valid():
            print('working   ')
            user = form.save(commit=False)
            user.is_creator = True
            user.save()
            user.save()
            creator = Creator.objects.create(user=user,bio=form.cleaned_data.get('bio'),location=form.cleaned_data.get('location'),academic_level=form.cleaned_data.get('academic_level')) 
            urban = forms.ModelChoiceField(County.objects.filter(county=countyid))
            creator.refresh_from_db()
            creator.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
        
        return redirect('creatorlogin')
        # return render(request, 'curriculum.html')
       
    else:
        form = CreatorSignUpForm()
    return render(request, 'registration/creator_registration_form.html', {'form': form})



def contract(request):
    with open('cm.pdf', 'r') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response
    pdf.closed


def new_group(request):
    current_user = request.user
    if request.method =='POST':
        form = GroupForm(request.POST, request.FILES)


        if form.is_valid():
            group = form.save(commit=False)

            group.save()
            return redirect('groups')

    else:
        form = GroupForm()
    return render(request, 'new_group.html', {"form":form})

def profile(request):
    current_user=request.user
    try:
        profis=Profile.objects.filter(user=current_user)[0:1]
        user_projects=Projects.objects.filter(user=current_user)
    except Exception as e:
        raise  Http404()
    if request.method=='POST':
        form=UpdateForm(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
        return redirect('profile')
    else:
        form=UpdateForm()
    return render(request,'creator_profile.html', {'form':form,'profile':profis,'projects':user_projects})



def creator_content(request):
    current_user=request.user
    try:
        user_projects=Projects.objects.filter()
    except Exception as e:
        raise  Http404()
    return render(request,'creator_content.html', {'projects':user_projects})
    

def sponsor(request):
    current_user = request.user
    categories = Category.objects.all()
    return render(request, "sponsor.html", {'categories': categories})

def sponsor_reports(request):
    projects = Projects.objects.all()
    return render(request, 'repports.html', {'projects': projects})

def creator(request):
    title = 'creator'

    return render(request, "curriculum.html", {"title": title})

def script(request, id):
    current_user = request.user
    form = ScriptForm() 
    
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES)
        if form.is_valid():
            script = form.save(commit=False)
            script.user_id =request.user.id
            script.save()

        return redirect("curriculum")

    else:
        form = ScriptForm()                    
        
    return render(request, 'script.html', {"user": current_user, "form": form})  


def get_video_id(url):
	prsed = urlparse(url)
	params = parse_qs(prsed.query)
	return params.get('v')[0]


def report(request, video_id):
    data = get_video_stats(video_id)
    print(data)
    return render(request, 'report.html', {
        'viewCount': data['viewCount'],
    })

def logout(request):
    dj_logout(request)
    return redirect('login')



def creator_home(request):
    title = 'Home'
    return render(request, "creator_home.html", {"title": title})


def post(request):
    current_user=request.user
    if request.method=='POST':
        form =PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user
            post.save()
        return redirect("profile")
    else:
        form=PostForm()
    return render(request,'post_content.html',{'form':form})






def curriculum(request):
    current_user = request.user
    user = User.objects.get(id=request.user.id)
    all_categories = CurriculumCategory.objects.all()
    return render(request,'curriculum.html', {"all_categories": all_categories})




def new_member(request):
    current_user = request.user
    if request.method =='POST':
        form = MemberForm(request.POST, request.FILES)

        if form.is_valid():
            group = form.save(commit=False)


            group.save()
            return redirect('groups')

    else:
        form = MemberForm()
    return render(request, 'new_member.html', {"form":form})


def resource(request):
    current_user=request.user
    if request.method == 'POST':
        form=ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource=form.save(commit=False)
            resource.sponsor_id =current_user.id
            resource.save()
            form=ResourceForm()
        return redirect("sponsor")

    else:
        form=ResourceForm()

    return render(request,'resource.html',{"form":form})



def children(request, id):
    resources=Resource.objects.filter(category_id=id)
    return render(request,'children.html',{'resources':resources})



def creator_script(request, id):
    scripts=Script.objects.filter(category_id=id)
    return render(request,'scripts.html',{'scripts':scripts})



def teenager(request):
    resources=Resource.objects.all()
    return render(request,'teenagers.html',{'resources':resources})


def groups(request):
    print("-" * 30)
    print("Hello")
    groups= Group.objects.all()
    
    print(groups)
    return render(request,'groups.html',{'groups':groups})

def members(request):
    print("-" * 30)
    print("Hello")
    members= Members.objects.all()
    
    print(members)
    return render(request,'members.html',{'members':members})

def creatorsignout(request):
    logout(request)
    return redirect('login')


def upload_scripts(request):
    scripts=Script.objects.all()
    print('-' * 30)
    print(scripts)
    return render(request,'scripts.html',{'scripts':scripts})


def contract(request):
    print("-" * 30)
    print("Hello")
    # contract= Group.objects.all()
    
    print(groups)
    return render(request,'contract.html',{'contract':contract})





