from django.http import JsonResponse
from .models import SiteLogo, MenuItem, Category, ProductLine, Card, GenderBanner, CarouselItem, LandingVideoBlock
from django.shortcuts import render
from .models import BrandBlock
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import BiruttiCategory
from .models import ShopCategory
from .models import Product, ProductColor
from collections import defaultdict


def site_logo_api(request):
    logo_obj = SiteLogo.objects.first()
    return JsonResponse({
        "logo_url": logo_obj.logo.url if logo_obj and logo_obj.logo else None
    })

def category_list_api(request):
    data = {
        "men": [],
        "women": [],
        "kids": [],
    }

    for cat in Category.objects.all():
        data[cat.gender].append({
            "name": cat.name,
            "link": cat.link,
        })

    return JsonResponse(data)

def get_menu_structure(request):
    menu_items = MenuItem.objects.filter(parent=None, is_active=True)
    
    def get_children(item):
        children = MenuItem.objects.filter(parent=item, is_active=True)
        return [{
            'title': child.title,
            'link': child.link,
            'children': get_children(child)
        } for child in children]
    
    menu_structure = [{
        'title': item.title,
        'link': item.link,
        'children': get_children(item)
    } for item in menu_items]
    
    return JsonResponse({'menu': menu_structure})

def get_categories(request):
    def get_subcategories(category):
        subcats = Category.objects.filter(parent=category, is_active=True).order_by('order', 'name')
        return [{
            "name": subcat.name,
            "link": subcat.link or f"/{category.gender.lower()}/{subcat.name.lower()}"
        } for subcat in subcats]

    response_data = {
        "men": [],
        "women": [],
        "kids": [],
        "pages": []
    }

    # Get all main categories (without parents)
    main_categories = Category.objects.filter(parent=None, is_active=True).order_by('order', 'name')
    
    for category in main_categories:
        category_data = {
            "name": category.name,
            "link": category.link,
            "subcategories": get_subcategories(category)
        }
        
        if category.gender == 'MEN':
            response_data["men"].append(category_data)
        elif category.gender == 'WOMEN':
            response_data["women"].append(category_data)
        elif category.gender == 'KIDS':
            response_data["kids"].append(category_data)
        elif category.gender == 'PAGE':
            response_data["pages"].append(category_data)
    
    return JsonResponse(response_data)

def get_product_lines(request):
    product_lines = ProductLine.objects.filter(parent=None, is_active=True)
    
    def get_line_data(line):
        sublines = ProductLine.objects.filter(parent=line, is_active=True)
        return {
            'name': line.name,
            'sublines': [get_line_data(sub) for sub in sublines]
        }
    
    result = {}
    for gender in ['men', 'women', 'kids']:
        gender_lines = product_lines.filter(gender=gender)
        result[gender] = [get_line_data(line) for line in gender_lines]
    
    return JsonResponse(result)

def cards_api(request):
    cards = Card.objects.filter(is_active=True).order_by('order')
    data = [
        {
            "title": card.title,
            "image": card.image.url if card.image else "",
            "link": card.link,
        }
        for card in cards
    ]
    return JsonResponse({"cards": data})

def index(request):
    return render(request, 'index.html')

def menu_categories_api(request):
    categories = Category.objects.filter(parent=None, is_active=True).order_by('order')
    data = {
        "categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "link": cat.link,
                "subcategories": [
                    {
                        "id": sub.id,
                        "name": sub.name,
                        "link": sub.link
                    }
                    for sub in cat.subcategories.filter(is_active=True).order_by('order')
                ]
            }
            for cat in categories
        ]
    }
    return JsonResponse(data)

def brands_block_api(request):
    block = BrandBlock.objects.prefetch_related('brands').first()
    if not block:
        return JsonResponse({"subtitle": "", "brands": []})
    return JsonResponse({
        "subtitle": block.subtitle,
        "brands": [
            {"name": b.name, "link": b.link}
            for b in block.brands.order_by('order')
        ]
    })

def gender_banners_api(request):
    banners = GenderBanner.objects.filter(is_active=True).order_by('order')
    data = [
        {
            "gender": b.gender,
            "title": b.title,
            "image": b.image.url if b.image else "",
            "link": b.link,
            "button_text": b.button_text,
        }
        for b in banners
    ]
    return JsonResponse({"banners": data})

def carousel_api(request):
    items = CarouselItem.objects.filter(is_active=True).order_by('order')
    data = [
        {
            "title": item.title,
            "image": item.image.url if item.image else "",
            "price": item.price,
            "link": item.link,
        }
        for item in items
    ]
    return JsonResponse({"carousel": data})

def landing_video_block_api(request):
    block = LandingVideoBlock.objects.filter(is_active=True).order_by('order').first()
    if not block:
        return JsonResponse({"block": None})
    videos = [
        {
            "video": v.video.url if v.video else "",
            "video_url": v.video_url,
        }
        for v in block.videos.filter(is_active=True).order_by('order')
    ]
    return JsonResponse({
        "block": {
            "title": block.title,
            "description": block.description,
            "button_text": block.button_text,
            "button_link": block.button_link,
            "videos": videos,
        }
    })


def contacts(request):
    return render(request, 'contacts.html')

def about_html(request):
    return render(request, 'about.html')

@api_view(['GET'])
def get_about_data(request):
    about_settings = AboutSettings.objects.first()
    about_sections = AboutSection.objects.all()
    video_banner = VideoBanner.objects.filter(is_active=True).first()

    settings_data = {
        'title': about_settings.title if about_settings else '',
        'subtitle': about_settings.subtitle if about_settings else '',
        'intro_text_1': about_settings.intro_text_1 if about_settings else '',
        'intro_text_2': about_settings.intro_text_2 if about_settings else '',
    }

    sections_data = []
    for section in about_sections:
        sections_data.append({
            'title': section.title,
            'description': section.description,
            'image': request.build_absolute_uri(section.image.url) if section.image else None,
            'link_text': section.link_text,
            'link_url': section.link_url,
            'image_on_left': section.image_on_left
        })

    video_data = {
        'video_url': request.build_absolute_uri(video_banner.video.url) if video_banner and video_banner.video else None
    }

    return Response({
        'settings': settings_data,
        'sections': sections_data,
        'video': video_data
    })

def shop_view(request):
    return render(request, 'shop.html')

@api_view(['GET'])
def get_category_subcategories(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        
        subcategories = category.subcategories.all()
        data = {
            'category_name': category.name,
            'subcategories': [
                {
                    'id': sub.id,
                    'name': sub.name,
                    'link': sub.link
                } for sub in subcategories
            ]
        }
        return Response(data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)

def birutti_menu_api(request):
    categories = []
    for cat in BiruttiCategory.objects.all():
        subcategories = []
        for sub in cat.subcategories.all():
            subsubcategories = [
                {"id": subsub.id, "name": subsub.name}
                for subsub in sub.subsubcategories.all()
            ]
            subcategories.append({
                "id": sub.id,
                "name": sub.name,
                "subsubcategories": subsubcategories
            })
        categories.append({
            "id": cat.id,
            "name": cat.name,
            "subcategories": subcategories
        })
    return JsonResponse({"categories": categories})

@api_view(['GET'])
def shop_menu_api(request):
    categories = ShopCategory.objects.filter(is_active=True).order_by('order')
    menu_data = {}
    for category in categories:
        subcategories = category.subcategories.filter(is_active=True).order_by('order')
        subcategory_list = []
        for subcategory in subcategories:
            subsubcategories = subcategory.subsubcategories.filter(is_active=True).order_by('order')
            subsubcategory_data = []
            for subsubcategory in subsubcategories:
                subsubsubcategories = [
                    {"id": sss.id, "name": sss.name}
                    for sss in subsubcategory.subsubsubcategories.filter(is_active=True).order_by('order')
                ]
                subsubcategory_data.append({
                    'id': subsubcategory.id,
                    'name': subsubcategory.name,
                    'link': subsubcategory.link,
                    'subsubsubcategories': subsubsubcategories
                })
            subcategory_list.append({
                'name': subcategory.name,
                'link': subcategory.link,
                'image': request.build_absolute_uri(subcategory.image.url) if subcategory.image else None,
                'caption': subcategory.caption,
                'subsubcategories': subsubcategory_data
            })
        category_key = category.name.lower()
        if category_key == 'man':
            category_key = 'men'
        menu_data[category_key] = {
            'name': category.name,
            'link': category.link,
            'list': [sub['name'] for sub in subcategory_list],
            'subcategories': subcategory_list,
            'mega': {
                sub['name']: {
                    'cols': [
                        {
                            'title': 'Categories',
                            'items': [item['name'] for item in sub['subsubcategories']]
                        }
                    ],
                    'image': {
                        'src': sub['image'] if 'image' in sub and sub['image'] else None,
                        'alt': sub['name'],
                        'link': sub['link'] if 'link' in sub and sub['link'] else '#',
                        'caption': sub['caption'] if 'caption' in sub and sub['caption'] else ''
                    }
                } for sub in subcategory_list
            }
        }
    return Response(menu_data)

def category_products_view(request):
    return render(request, 'category-products.html')

def product_view(request):
    return render(request, 'product.html')

def women_view(request):
    return render(request, 'women.html')

def kids_view(request):
    return render(request, 'kids.html')

@api_view(['GET'])
def products_api(request):
    subsubcat_id = request.GET.get('subsubcat_id')
    gender = request.GET.get('gender')
    products = Product.objects.all()
    if subsubcat_id:
        products = products.filter(shop_subsubcategory_id=subsubcat_id)
    if gender:
        products = products.filter(shop_category__gender__iexact=gender)
    subsubsubcategory_id = request.GET.get('subsubsubcategory_id')
    if subsubsubcategory_id:
        products = products.filter(shop_subsubsubcategory_id=subsubsubcategory_id)
    data = []
    for product in products:
        main_color = product.colors.first()
        if main_color:
            data.append({
                "id": product.id,
                "title": product.title,
                "price": str(main_color.price),
                "main_image": main_color.color_image.url if main_color.color_image else "",
            })
    return Response(data)

@api_view(['GET'])
def product_detail_api(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    # Найти рекомендации по той же shop_subsubcategory (или другой нужной категории)
    recommendations = Product.objects.filter(
        shop_subsubcategory=product.shop_subsubcategory
    ).exclude(id=product.id)[:8]

    recommendations_data = [
        {
            'id': rec.id,
            'title': rec.title,
            'main_image': rec.colors.first().color_image.url if rec.colors.exists() else '',
        }
        for rec in recommendations
    ]

    images = [request.build_absolute_uri(img.image.url) for img in product.images.all()]
    sizes_by_system = defaultdict(list)
    for size in product.size_objects.all():
        sizes_by_system[size.system].append(size.value)

    colors = [
        {
            'name': color.name,
            'color_image': request.build_absolute_uri(color.color_image.url) if color.color_image else "",
            'price': str(color.price),
            'images': [request.build_absolute_uri(img.image.url) for img in color.images.all()]
        }
        for color in product.colors.all()
    ]

    accordion_blocks = [
        {
            'title': block.title,
            'content_type': block.content_type,
            'text': block.text,
            'image': request.build_absolute_uri(block.image.url) if block.image else None,
        }
        for block in product.accordion_blocks.all()
    ]

    data = {
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'composition': product.composition,
        'images': images,
        'sizes': sizes_by_system,
        'colors': colors,
        'marketplace_links': [
            {
                'name': link.name,
                'url': link.url
            }
            for link in product.marketplace_links.all()
        ],
        'recommendations': recommendations_data,
        'accordion_blocks': accordion_blocks,
    }
    return Response(data)

def product_html(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(pk=product_id)
    return render(request, 'product.html', {'product': product})

def product_detail(request, id):
    return render(request, 'product.html')