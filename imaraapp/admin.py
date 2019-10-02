from django.contrib import admin
from .models import SponsorProfile, Script, CreatorProfile, Creator, Category, CurriculumCategory, Major, Minor, Counties, Urban

# Register your models here.

admin.site.register(Script)
admin.site.register(CreatorProfile)
admin.site.register(SponsorProfile)
admin.site.register(Creator)
admin.site.register(Counties)
admin.site.register(Urban)
admin.site.register(Major)
admin.site.register(Minor)
admin.site.register(Category)
admin.site.register(CurriculumCategory)
