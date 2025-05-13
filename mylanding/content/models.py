from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class LandingMedia(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class SiteLogo(models.Model):
    logo = models.FileField("Логотип", upload_to="logo/")

    class Meta:
        verbose_name = "Логотип"
        verbose_name_plural = "Логотип"

    def __str__(self):
        return "Логотип сайта"


class SiteSlogan(models.Model):
    slogan = models.CharField("Слоган", max_length=255)

    class Meta:
        verbose_name = "Слоган"
        verbose_name_plural = "Слоган"

    def __str__(self):
        return "Слоган сайта"
class CategoryGroup(models.Model):
    name = models.CharField("Название группы", max_length=100)

    class Meta:
        verbose_name = "Группа категорий"
        verbose_name_plural = "Группы категорий"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    link = models.CharField(max_length=200, blank=True, verbose_name="Ссылка")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name="Родительская категория")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class ProductLine(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
    ]

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.gender} - {self.name}"

class Card(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    image = models.ImageField("Картинка", upload_to="cards/")
    link = models.URLField("Ссылка", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

        
class BrandBlock(models.Model):
    subtitle = models.CharField("Подзаголовок", max_length=255, default="COLLEZIONE SPRING SUMMER MAN 2025")

class Brand(models.Model):
    block = models.ForeignKey(BrandBlock, on_delete=models.CASCADE, related_name="brands")
    name = models.CharField("Название бренда", max_length=100)
    link = models.CharField("Ссылка", max_length=200)
    order = models.PositiveIntegerField("Порядок", default=0)

class GenderBanner(models.Model):
    GENDER_CHOICES = [
        ('men', 'For Man'),
        ('women', 'For Women'),
        ('kids', 'For Children'),
    ]
    gender = models.CharField("Пол/Категория", max_length=10, choices=GENDER_CHOICES)
    title = models.CharField("Заголовок", max_length=100)
    image = models.ImageField("Картинка", upload_to="banners/")
    link = models.CharField("Ссылка", max_length=200)
    button_text = models.CharField("Текст кнопки", max_length=50, default="New in")
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_gender_display()} - {self.title}"

class CarouselItem(models.Model):
    title = models.CharField("Название", max_length=255)
    image = models.ImageField("Картинка", upload_to="carousel/")
    price = models.CharField("Цена", max_length=50)
    link = models.URLField("Ссылка", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Карусель: товар"
        verbose_name_plural = "Карусель: товары"

    def __str__(self):
        return self.title

class LandingVideoBlock(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание")
    button_text = models.CharField("Текст кнопки", max_length=100)
    button_link = models.URLField("Ссылка кнопки", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        verbose_name = "Видео-блок: текст"
        verbose_name_plural = "Видео-блоки: текст"

    def __str__(self):
        return self.title

class LandingVideoItem(models.Model):
    block = models.ForeignKey(LandingVideoBlock, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField("Видео", upload_to="landing_videos/", blank=True, null=True)
    video_url = models.URLField("Ссылка на видео (YouTube/Vimeo)", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Видео-блок: видео"
        verbose_name_plural = "Видео-блоки: видео"

    def __str__(self):
        return f"Видео для {self.block.title}"

class AboutSettings(models.Model):
    title = models.CharField(max_length=200, verbose_name="Main Title")
    subtitle = models.CharField(max_length=200, verbose_name="Subtitle (ABOUT HERMÈS)")
    intro_text_1 = models.TextField(verbose_name="First Intro Paragraph")
    intro_text_2 = models.TextField(verbose_name="Second Intro Paragraph")
    
    class Meta:
        verbose_name = "About Page Settings"
        verbose_name_plural = "About Page Settings"

    def __str__(self):
        return "About Page Settings"

class AboutSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Section Title")
    description = models.TextField(verbose_name="Section Description")
    image = models.ImageField(upload_to='about/', verbose_name="Section Image")
    link_text = models.CharField(max_length=100, default="FIND OUT MORE", verbose_name="Link Text")
    link_url = models.CharField(max_length=200, default="#", verbose_name="Link URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    image_on_left = models.BooleanField(default=False, verbose_name="Image on Left Side")

    class Meta:
        ordering = ['order']
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.title

class VideoBanner(models.Model):
    video = models.FileField(upload_to='videos/', verbose_name="Background Video")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    
    class Meta:
        verbose_name = "Video Banner"
        verbose_name_plural = "Video Banners"

    def __str__(self):
        return f"Video Banner {self.id}"


class BiruttiCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BiruttiSubCategory(models.Model):
    category = models.ForeignKey(BiruttiCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BiruttiSubSubCategory(models.Model):
    subcategory = models.ForeignKey(BiruttiSubCategory, related_name='subsubcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ShopCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссылка', default='')
    gender = models.CharField(max_length=10, choices=[('men', 'Men'), ('women', 'Women'), ('kids', 'Kids')], default='men')

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class ShopSubCategory(models.Model):
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссылка', default='')
    image = models.ImageField(upload_to='shop/subcategories/', null=True, blank=True)
    caption = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Shop Sub Category'
        verbose_name_plural = 'Shop Sub Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class ShopSubSubCategory(models.Model):
    subcategory = models.ForeignKey(ShopSubCategory, on_delete=models.CASCADE, related_name='subsubcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    link = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Shop Sub Sub Category'
        verbose_name_plural = 'Shop Sub Sub Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.subcategory.category.name} - {self.subcategory.name} - {self.name}"

class ShopSubSubSubCategory(models.Model):
    subsubcategory = models.ForeignKey(ShopSubSubCategory, on_delete=models.CASCADE, related_name='subsubsubcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    link = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Shop Sub Sub Sub Category'
        verbose_name_plural = 'Shop Sub Sub Sub Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.subsubcategory.subcategory.category.name} - {self.subsubcategory.subcategory.name} - {self.subsubcategory.name} - {self.name}"

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    composition = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    sizes_json = models.JSONField(default=dict, blank=True, null=True)
    marketplace_links = models.ManyToManyField('MarketplaceLink', blank=True)
    shop_category = models.ForeignKey('ShopCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    shop_subcategory = models.ForeignKey('ShopSubCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    shop_subsubcategory = models.ForeignKey('ShopSubSubCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    shop_subsubsubcategory = models.ForeignKey(
        'ShopSubSubSubCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    # Основные фото

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes')
    size = models.CharField(max_length=20)

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color_image = models.ImageField(upload_to='color_photos/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # images = models.ManyToManyField(ProductImage, blank=True)  # Можно удалить, если используешь ProductColorImage

class ProductColorImage(models.Model):
    color = models.ForeignKey(ProductColor, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='color_images/')

    def image_tag(self):
        if self.image:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{self.image.url}" style="max-height: 60px;" />')
        return ""
    image_tag.short_description = 'Preview'

class ProductColorSize(models.Model):
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)

class Size(models.Model):
    product = models.ForeignKey(Product, related_name='size_objects', on_delete=models.CASCADE)
    system = models.CharField(max_length=10, choices=[('EU', 'EU'), ('UK', 'UK'), ('US', 'US')])
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.system} - {self.value}"

class MarketplaceLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    def __str__(self):
        return self.name

class ProductAccordionBlock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accordion_blocks')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('image', 'Image')])
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='accordion_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.content_type})"

        