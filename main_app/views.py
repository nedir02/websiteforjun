import stripe
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from mywebsite import settings
from .forms import OrderForm, CustomerForm
from .models import Customer, Service, Order


def home(request):
    return render(request, 'main_app/home.html')


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'main_app/customer_list.html', {'customers': customers})


def service_list(request):
    services = Service.objects.all()
    return render(request, 'main_app/service_list.html', {'services': services})


@login_required
def create_order(request):
    # Retrieve the customer based on the logged-in user's email
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        messages.error(request, 'You need to create a customer profile first.')
        return redirect('create_customer')  # Redirect to customer creation if not found

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer  # Associate the order with the customer
            order.save()
            messages.success(request, 'Your order has been created successfully.')
            return redirect('mock_checkout', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'main_app/create_order.html', {'form': form})

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Create Stripe Checkout Session for payment processing
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': order.service.name,
                },
                'unit_amount': int(order.service.price * 100),  # Convert price to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payment-success/'),  # Redirect on success
        cancel_url=request.build_absolute_uri('/checkout/{}/'.format(order_id)),  # Redirect on cancel
    )

    # Render the checkout template with the Stripe session
    return render(request, 'main_app/checkout.html', {
        'order': order,
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY  # Set your Stripe public key
    })


def mock_checkout(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'main_app/checkout.html', {'order': order})


def payment_success(request):
    messages.success(request, 'Your payment was successful!')
    return render(request, 'main_app/payment_success.html')

def payment_cancel(request):
    messages.error(request, 'Your payment was canceled.')
    return render(request, 'main_app/payment_cancel.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Process the form data here (e.g., save it, send an email, etc.)
        # For now, we’ll just simulate success with a message

        messages.success(request, "Thank you for reaching out! We'll get back to you soon.")
        return redirect('contact')

    return render(request, 'main_app/contact.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main_app/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'main_app/login.html')


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Redirect to the home page after logout


# Add this view to your views.py
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')  # Redirect to the list of customers
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerForm()

    return render(request, 'main_app/register.html', {'form': form})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'main_app/service_detail.html', {'service': service})