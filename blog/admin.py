from django.contrib import admin
from .models import Post, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin


# Register your models here.
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)


# Category model의 name Field에 값이 입력되면 자동으로 slug가 만들어지게됨.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)