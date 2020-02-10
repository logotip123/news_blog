from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment


class CommentAdmin(admin.TabularInline):
    exclude = ('author',)
    fields = ('content', 'created_on')
    readonly_fields = ('created_on',)
    ordering = ('-created_on',)
    model = Comment
    extra = 0


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on', 'status')
    list_filter = ('author', 'status')
    exclude = ('slug',)
    summernote_fields = ('content',)
    search_fields = ('title', 'content', 'author')
    ordering = ('-created_on',)
    inlines = (CommentAdmin,)


admin.site.register(Post, PostAdmin)
