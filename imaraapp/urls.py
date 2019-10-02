from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^$', views.home, name="home"),
    # url(r'^api/', views.creator_list),
    url(r'^creator/content$', views.creator_content, name='creator-content'),
    url(r'^sponsor_reports/$', views.sponsor_reports, name='sponsor_reports'),
    url(r'^sponsorlogin/', views.sponsorlogin, name='sponsorlogin'),
    url(r'project/post/$',views.post,name='post'),
    url(r'^user/profile/$',views.profile,name='profile'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^sponsorsignup/$', views.sponsorsignup, name='sponsorsignup'),
    url(r'^creator/signup/$', views.creatorsignup, name='creatorsignup'),
    url(r'^creator/contract/$', views.contract, name='contract'),
    url(r'^sponsor/$', views.sponsor, name='sponsor'),
    url(r'^creator/$', views.creator, name='creator'),
    url(r'^new/group$', views.new_group, name='new-group'),
    url(r'^new/member$', views.new_member, name='new-member'),
    url(r'^creator/home$', views.creator_home, name='creator-home'),
    url(r'^curriculum/$', views.curriculum, name='curriculum'),
    url(r'^script/(\d+)/$', views.script, name='script'),
    url(r'^resource/$', views.resource, name='resource'),
    url(r'^display/(\d+)/$', views.children, name='display-children'),
    url(r'^display/teenager/$', views.teenager, name='display-teenager'),
    url(r'^display/scripts/(\d+)/$', views.creator_script, name='display-scripts'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^get_video_stats/(?P<video_id>.+)$', views.report, name='stats'),
    url(r'^members/$', views.members, name='members'),
    url(r'^rooms/$', views.chat, name='chat'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.roomm, name='roomm'),
    url(r'^view/scripts/$', views.upload_scripts, name="upload_scripts"),
    url(r'^creator/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^creator/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
