from django.contrib import admin
from .models import Book,AuthorBio,Review,Profile,ProfileStatus
# Register your models here.

admin.site.register(Book)
admin.site.register(AuthorBio)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(ProfileStatus)