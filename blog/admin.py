from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display        =   ('id', 'title', 'author', 'created', 'updated', 'status')
    list_display_links  =   ('id', 'title', 'author', )
    list_filter         =   ('created', 'updated', 'status', 'author', )
    search_fields       =   ('title', 'author', 'body', )
    prepopulated_fields =   {'slug':('title', )}
    list_editable       =   ('status', )
    date_hierarchy      =   ('created')
    # list_per_page       =   25


admin.site.register(Post, PostAdmin)