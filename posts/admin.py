from django.contrib import admin
from posts.models import Post, Category, Tag, Comment
from django.utils.html import format_html

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;"/>'.format(object.image.url))

    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'title', 'user', 'publishing_date')
    list_display_links = ('id','thumbnail', 'user','title')
    list_filter = ('title','user')
    # list_editable = ('is_published',)
    search_fields =('user', 'title')
    list_per_page = 10

class AdminComment(admin.ModelAdmin):
    list_filter = ('publishing_date',)
    search_fields = ('name','email','content','post__title')

    class Meta:
        model = Comment






admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, AdminComment)