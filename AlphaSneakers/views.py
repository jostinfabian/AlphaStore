from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from AlphaSneakers.models import Sneaker, Category, Brand, Promotion, BlogPost, SocialPost


# Create your views here.


def home_view(request):
    featured_sneakers = Sneaker.objects.filter(featured=True)
    promotions = Promotion.objects.all()
    context = {
        'featured_sneakers': featured_sneakers,
        'promotions': promotions,
    }
    return render(request, "AlphaSneakers/home.html", context)


def search(request):
    query = request.GET.get('query')
    if query:
        sneakers = Sneaker.objects.filter(name__icontains=query)
    else:
        sneakers = Sneaker.objects.none()
    context = {
        'sneakers': sneakers,
    }
    return render(request, 'AlphaSneakers/product_list.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(subject, message, email, ['contact@alphastore.com'], fail_silently=False)
        return redirect('contact')
    return render(request, 'AlphaSneakers/contact.html', {})

def product_list(request):
    sneakers = Sneaker.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # Filtros para buscar y filtrar productos
    category_filter = request.GET.get('category')
    if category_filter:
        sneakers = sneakers.filter(category__name=category_filter)
    brand_filter = request.GET.get('brand')
    if brand_filter:
        sneakers = sneakers.filter(brand__name=brand_filter)
    size_filter = request.GET.get('size')
    if size_filter:
        sneakers = sneakers.filter(size=size_filter)
    price_filter = request.GET.get('price')
    if price_filter:
        sneakers = sneakers.filter(price__lte=price_filter)

    context = {
        'sneakers': sneakers,
        'categories': categories,
        'brands': brands,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'size_filter': size_filter,
        'price_filter': price_filter,
    }
    return render(request, 'AlphaSneakers/product_list.html', context)


def product_detail(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)
    images = sneaker.sneakerimage_set.all()
    context = {
        'sneaker': sneaker,
        'images': images,
    }
    return render(request, 'AlphaSneakers/product_detail.html', context)


def add_to_cart(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)
    # Agrega el producto al carrito de compras
    # (puedes utilizar la sesión de Django o un modelo de base de datos para almacenar los productos del carrito)
    return redirect('cart')


def cart(request):
    # Recupera los productos del carrito de compras
    cart_items = request.session.get('cart', {})
    # Calcula el precio total del carrito
    total_price = 0
    for pk, quantity in cart_items.items():
        sneaker = get_object_or_404(Sneaker, pk=pk)
        total_price += sneaker.price * quantity
    # Procesa la actualización de la cantidad de cada producto o la eliminación de productos del carrito
    if request.method == 'POST':
        # Actualiza la cantidad de cada producto
        for pk, quantity in cart_items.items():
            new_quantity = int(request.POST.get(f'quantity_{pk}'))
            if new_quantity > 0:
                cart_items[pk] = new_quantity
            else:
                del cart_items[pk]
        request.session['cart'] = cart_items
        return redirect('cart')
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'AlphaSneakers/cart.html', context)


def new_arrivals(request):
    sneakers = Sneaker.objects.order_by('-created_at')[:10]
    context = {
        'sneakers': sneakers,
    }
    return render(request, 'AlphaSneakers/new_arrivals.html', context)


def inspiration(request):
    # Recupera los últimos 10 artículos de blog publicados
    blog_posts = BlogPost.objects.order_by('-published_at')[:10]
    # Recupera las últimas 10 publicaciones de redes sociales
    social_posts = SocialPost.objects.order_by('-published_at')[:10]
    context = {
        'blog_posts': blog_posts,
        'social_posts': social_posts,
    }
    return render(request, 'AlphaSneakers/inspiration.html', context)
