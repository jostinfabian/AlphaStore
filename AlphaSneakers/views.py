from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from AlphaSneakers.models import *


# Create your views here.


def home_view(request):
    featured_sneakers = Sneaker.objects.filter()  # Recupera los productos destacados
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


#  Una vista para mostrar la lista de todos los productos disponibles, con filtros para permitir a los usuarios buscar y filtrar productos por categoría, marca, tamaño y precio.
def product_list(request):
    # Recupera los productos de la base de datos
    sneakers = Sneaker.objects.all()
    # Filtra los productos en función de las categorías seleccionadas
    categories = request.GET.getlist('category')
    if categories:
        sneakers = sneakers.filter(category__in=categories)
    # Filtra los productos en función de las marcas seleccionadas
    brands = request.GET.getlist('brand')
    if brands:
        sneakers = sneakers.filter(brand__in=brands)
    # Filtra los productos en función de los tamaños seleccionados
    sizes = request.GET.getlist('size')
    if sizes:
        sneakers = sneakers.filter(size__in=sizes)
    # Filtra los productos en función de los precios seleccionados
    prices = request.GET.getlist('price')
    if prices:
        if '0-100' in prices:
            sneakers = sneakers.filter(price__gte=0, price__lte=100)
        if '100-200' in prices:
            sneakers = sneakers.filter(price__gte=100, price__lte=200)
        if '200-300' in prices:
            sneakers = sneakers.filter(price__gte=200, price__lte=300)
        if '300-400' in prices:
            sneakers = sneakers.filter(price__gte=300, price__lte=400)
        if '400-500' in prices:
            sneakers = sneakers.filter(price__gte=400, price__lte=500)
        if '500-600' in prices:
            sneakers = sneakers.filter(price__gte=500, price__lte=600)
        if '600-700' in prices:
            sneakers = sneakers.filter(price__gte=600, price__lte=700)
        if '700-800' in prices:
            sneakers = sneakers.filter(price__gte=700, price__lte=800)
        if '800-900' in prices:
            sneakers = sneakers.filter(price__gte=800, price__lte=900)
        if '900-1000' in prices:
            sneakers = sneakers.filter(price__gte=900, price__lte=1000)
        if '1000-' in prices:
            sneakers = sneakers.filter(price__gte=1000)
    context = {
        'sneakers': sneakers,
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
