from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import SponsorProfile, Script,Profile,Projects,Resource,Group,Members, Creator, Major, Minor, Counties, Urban
from django.contrib.auth import get_user_model




class SponsorSignUpForm(UserCreationForm):
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    email= forms.CharField(required=True)
    username= forms.CharField(required=True)
    address= forms.CharField(required=True)
    organization= forms.CharField(required=True)
    phone= forms.CharField(required=True)
   

    

    class Meta:
        model = get_user_model()

        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'organization', 'phone']


class MajorForm(forms.ModelForm):

    class Meta:
        model = Major
        fields = ['skill']

class MinorForm(forms.ModelForm):

    class Meta:
        model = Minor
        fields = ['skill']


class CreatorSignUpForm(UserCreationForm):
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    stage_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email= forms.CharField(required=True)
    username= forms.CharField(required=True)
    bio= forms.CharField(required=True)
    major_skill=forms.ModelChoiceField(Major.objects.all(), required=True)
    minor_skill=forms.ModelChoiceField(Minor.objects.all(), required=False)
    county= forms.ModelChoiceField(Counties.objects.all(), required=True)
    urban_centre = forms.ModelChoiceField(Urban.objects.all())
    academic_level= forms.CharField(required=True)
   
    

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name','stage_name', 'username','email','phone','bio','major_skill','minor_skill', 'county','urban_centre','academic_level']



class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['group_name', 'description', 'email']

class MemberForm(forms.ModelForm):

    class Meta:
        model = Members
        fields = ['name', 'email','major_skill', 'group']



class PostForm(forms.ModelForm):
    class Meta:
        model=Projects
        exclude=['user','design','usability','content']


class UpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user']



class ScriptForm(forms.ModelForm):

    class Meta:
        model = Script
        exclude=['user']


class ResourceForm(forms.ModelForm):
    class Meta:
        model= Resource
        exclude=['sponsor_id']
