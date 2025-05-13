from django.contrib import admin
from .models import SiteLogo, Category
from .models import BrandBlock, Brand
from .models import GenderBanner
from .models import CarouselItem
from .models import LandingVideoBlock, LandingVideoItem
from .models import AboutSettings, AboutSection, VideoBanner
from .models import BiruttiCategory, BiruttiSubCategory, BiruttiSubSubCategory
from .models import ShopCategory, ShopSubCategory, ShopSubSubCategory
from .models import Product, ProductColor, ProductColorImage, ProductColorSize, ProductImage, ProductSize
from .models import Size, MarketplaceLink, ProductAccordionBlock
from .models import ShopSubSubSubCategory
import nested_admin

@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteLogo.objects.exists()

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    fk_name = 'parent'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'link')
    inlines = [CategoryInline]



class BrandInline(admin.TabularInline):
    model = Brand
    extra = 1

@admin.register(BrandBlock)
class BrandBlockAdmin(admin.ModelAdmin):
    inlines = [BrandInline]

@admin.register(GenderBanner)
class GenderBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'gender', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('gender', 'is_active')
    search_fields = ('title',)

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'price')
    search_fields = ('title',)

class LandingVideoItemInline(admin.TabularInline):
    model = LandingVideoItem
    extra = 1

@admin.register(LandingVideoBlock)
class LandingVideoBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [LandingVideoItemInline]

@admin.register(AboutSettings)
class AboutSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow only one instance
        if self.model.objects.exists():
            return False
        return True

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'image_on_left']
    list_editable = ['order', 'image_on_left']
    ordering = ['order']

@admin.register(VideoBanner)
class VideoBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active']
    list_editable = ['is_active']

    def has_add_permission(self, request):
        # Allow only one active video banner
        if self.model.objects.filter(is_active=True).exists():
            return False
        return True

class BiruttiSubSubCategoryInline(admin.TabularInline):
    model = BiruttiSubSubCategory
    extra = 1

class BiruttiSubCategoryInline(admin.TabularInline):
    model = BiruttiSubCategory
    extra = 1

class BiruttiSubCategoryAdmin(admin.ModelAdmin):
    inlines = [BiruttiSubSubCategoryInline]

class BiruttiCategoryAdmin(admin.ModelAdmin):
    inlines = [BiruttiSubCategoryInline]

admin.site.register(BiruttiCategory, BiruttiCategoryAdmin)
admin.site.register(BiruttiSubCategory, BiruttiSubCategoryAdmin)
admin.site.register(BiruttiSubSubCategory)

@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ShopSubCategory)
class ShopSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ShopSubSubCategory)
class ShopSubSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'order', 'is_active')
    list_filter = ('is_active', 'subcategory__category', 'subcategory')
    search_fields = ('name', 'subcategory__name', 'subcategory__category__name')
    prepopulated_fields = {'slug': ('name',)}

# Inline для фото цвета
class ProductColorImageInline(nested_admin.NestedTabularInline):
    model = ProductColorImage
    extra = 1

# Inline для цвета
class ProductColorInline(nested_admin.NestedStackedInline):
    model = ProductColor
    extra = 1
    inlines = [ProductColorImageInline]

# Inline для фото товара (основные фото)
class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 1

# Inline для размеров (если нужно)
class ProductSizeInline(nested_admin.NestedTabularInline):
    model = ProductSize
    extra = 1

# Регистрация ProductColorImage отдельно (чтобы можно было добавлять фото к цвету)
@admin.register(ProductColorImage)
class ProductColorImageAdmin(admin.ModelAdmin):
    list_display = ['color', 'image_tag']
    readonly_fields = ['image_tag']

# Регистрация ProductColor отдельно (чтобы можно было добавлять фото к цвету через Inline)
@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    inlines = [ProductColorImageInline]
    list_display = ['product', 'name', 'color_image', 'price']

# Регистрация основного товара
class ProductAccordionBlockInline(nested_admin.NestedTabularInline):
    model = ProductAccordionBlock
    extra = 1

class SizeInline(nested_admin.NestedTabularInline):
    model = Size
    extra = 1

class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'shop_category', 'shop_subcategory', 'shop_subsubcategory', 'shop_subsubsubcategory')
    fields = (
        'title',
        'description',
        'composition',
        'category',
        'shop_category',
        'shop_subcategory',
        'shop_subsubcategory',
        'shop_subsubsubcategory',
        'sizes_json',
        'marketplace_links',
    )
    inlines = [SizeInline, ProductImageInline, ProductSizeInline, ProductColorInline, ProductAccordionBlockInline]
    filter_horizontal = ['marketplace_links']

admin.site.register(Size)
admin.site.register(MarketplaceLink)
admin.site.register(Product, ProductAdmin)

class ShopSubSubSubCategoryInline(admin.TabularInline):
    model = ShopSubSubSubCategory
    extra = 1

class ShopSubSubCategoryAdmin(admin.ModelAdmin):
    inlines = [ShopSubSubSubCategoryInline]
    list_display = ('name', 'subcategory', 'order', 'is_active')
    list_filter = ('is_active', 'subcategory__category', 'subcategory')
    search_fields = ('name', 'subcategory__name', 'subcategory__category__name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ShopSubSubSubCategory)
class ShopSubSubSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subsubcategory', 'order', 'is_active')
    list_filter = ('is_active', 'subsubcategory__subcategory__category', 'subsubcategory__subcategory', 'subsubcategory')
    search_fields = ('name', 'subsubcategory__name', 'subsubcategory__subcategory__name')
    prepopulated_fields = {'slug': ('name',)}