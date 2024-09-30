from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)
    inlines = [VersionInline]


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_name', 'is_current',)
    list_filter = ('is_current',)
