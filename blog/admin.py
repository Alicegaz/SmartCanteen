from blog.forms import PostForm
from django.contrib import admin
from .models import Post, Ingredient
from sortedm2m.fields import SortedManyToManyField


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    fieldsets = (
        (None, {'fields': ('name', 'ingredients')}),
    )

admin.site.register(Ingredient)
admin.site.register(Post, PostAdmin)

# class PostIngredientInline(admin.TabularInline):
#   model = PostIngredient


# class PostAdmin(admin.ModelAdmin):
# inlines = [PostIngredientInline]


# class IngredientAdmin(admin.ModelAdmi):
# inlines = [PostIngredientInline]


# class IngredientAdmin(admin.ModelAdmin):
# inlines = [PostIngredientInline]

# admin.site.register(Post, PostAdmin)
# admin.site.register(Ingredient, IngredientAdmin)
# Register your models here.
