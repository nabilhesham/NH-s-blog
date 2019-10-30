from django.contrib import admin
from .models import Post, Profile, Images, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

admin.site.register(Post, PostAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')

admin.site.register(Profile, ProfileAdmin)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')

admin.site.register(Images, ImagesAdmin)

admin.site.register(Comment)
