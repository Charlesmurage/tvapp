from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from urllib.parse import urlparse, parse_qs

class User(AbstractUser):
    is_sponsor = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)


class SponsorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,related_name='sponsor_info')
    first_name= models.CharField(max_length=500)
    last_name= models.CharField(max_length=500)
    email= models.CharField(max_length=500)
    address= models.CharField(max_length=500)
    organization= models.CharField(max_length=500)
    phone= models.CharField(max_length=500)
    avatar = models.ImageField(upload_to='avatar', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messsages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class CreatorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE,related_name='creator_info')
    avatar = models.ImageField(upload_to='avatar', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Counties(models.Model):
    county = models.CharField(max_length=100)

    def __str__(self):
        return self.county

class Urban(models.Model):
    urban_centre = models.CharField(max_length=100, null=True)
    county = models.ForeignKey(Counties, null=True)

    def __str__(self):
        return self.urban_centre

class Major(models.Model):
    skill = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.skill

class Minor(models.Model):
    skill = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.skill




class Creator(models.Model):
    '''
    creating a profile model for each creator
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='creator_profile')
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    stage_name = models.CharField(max_length=100, null=True)
    email= models.CharField(max_length=500, blank=True)
    Phone = models.CharField(max_length=10, blank=False, null=True)
    bio = models.TextField(max_length=500, blank=True)
    county = models.ForeignKey(Counties,null=True)
    urban_centre = models.ForeignKey(Urban,null=True)
    major_skill = models.ForeignKey(Major, null=True)
    major_skill = models.ForeignKey(Minor)
    academic_level= models.CharField(max_length=500, blank=True)





class Projects(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to='projects/')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField(max_length=320)
    link=models.URLField(max_length=60)
    date=models.DateField(auto_now=True)
    screen1=models.ImageField(upload_to='screenshot/',blank=True)
    screen2=models.ImageField(upload_to='screenshot/',blank=True)

    class Meta:
        ordering=['-name']

    def __str__(self):
        self.name

    @property
    def get_video_id(self):
        prsed = urlparse(self.link)
        params = parse_qs(prsed.query)
        return params.get('v')[0]


    @classmethod
    def search_project(cls,word):
        searched=cls.objects.filter(name__icontains=word)
        return searched

class Category(models.Model):
    name = models.CharField(max_length=50)
    date_added = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Script(models.Model):
    script_title = models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='images/', null=True,blank=True)
    synopsis = models.TextField(max_length=500)
    date=models.DateField(auto_now=True)
    budget = models.CharField(max_length=200)
    category_id = models.ForeignKey(Category, default=0)
    # test = models.TextField(default="Hello")


    def __str__(self):
        return self.script_title


class Profile(models.Model):
    profile=models.ImageField(upload_to='profile/')
    bio=models.CharField(max_length=60)
    major_skill = models.ForeignKey(Major)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    
    
    class Meta:
        ordering=['-profile']

    
    # def __str__(self):
    #         return f' {self.name} Script'


    # def create_script(self):
    #     self.save()

    # def delete_script(self):
    #     self.delete()
class CurriculumCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

        


class Resource(models.Model):
    image=models.ImageField(upload_to='resource/',default="no image")
    title=models.CharField(max_length=50)
    description=models.TextField()
    url=models.CharField(max_length=250)    
    category_id=models.ForeignKey(CurriculumCategory,default=0)
    sponsor_id = models.IntegerField()

    def  __str__(self):
        return f' {self.name} Resource'

    def save_resource(self):
        save.resource()
 
    
class Group(models.Model):
    group_name = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField(max_length=100)
    def __str__(self):
        return self.group_name


class Members(models.Model):
    name =models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=40)
    major_skill = models.ForeignKey(Major, null=True)
    group = models.ForeignKey(Group)
    
    

