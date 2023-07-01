import random

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                customer = Customer.objects.create(user=user)
                return redirect('login')
        context = {"form": form}
        return render(request, "register.html", context=context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("main")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect("dashboard")
                else:
                    return redirect('main')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, "login.html", context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def products(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Permission Denied")
    queryset = Product.objects.all()
    context = {"products": queryset}
    return render(request, "admininterface.html", context=context)


@login_required(login_url='login')
def customer(request, pk):
    mycustomer = Customer.objects.get(id=pk)
    orders = mycustomer.orders.all()
    total_orders = orders.count()
    context = {"mycustomer": mycustomer, "orders": orders, "total_orders": total_orders}
    return render(request, "customer.html", context=context)



@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')

    cart_items = OrderItem.objects.filter(order=order)

    context = {"form": form, "order": order, "cart_items": cart_items}
    return render(request, "order_form.html", context=context)


@login_required(login_url='login')
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    context = {"form": form}
    return render(request, "add.html", context=context)


@login_required(login_url='login')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('/products/')
    context = {"item": product}
    return render(request, "deleteproduct.html", context=context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard/')
    context = {"item": order}
    return render(request, "delete.html", context=context)


@login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/dashboard/')
    context = {"item": customer}
    return render(request, "delete_customer.html", context=context)


def homeadmin(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
        customers = Customer.objects.all()

        total_customers = customers.count()
        total_orders = orders.count()
        delivered = orders.filter(status="Delivered").count()
        pending = orders.filter(status="Pending").count()
        context = {"orders": orders, "customers": customers, "total_orders": total_orders,
                   "total_customers": total_customers, "delivered": delivered, "pending": pending}
        return render(request, "dashboard.html", context=context)
    else:
        return HttpResponseForbidden("Permission denied")


def laptops(request):
    queryset = Product.objects.filter(category="Laptop")
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    context = {"laptops": queryset, "sort_by": sort_by}
    return render(request, "laptops.html", context=context)


def phones(request):
    queryset = Product.objects.filter(category="Phone")
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    context = {"phones": queryset, "sort_by": sort_by}
    return render(request, "phones.html", context=context)


def tvs(request):
    queryset = Product.objects.filter(category="TV")
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    context = {"tvs": queryset, "sort_by": sort_by}
    return render(request, "tvs.html", context=context)


def main_page(request):
    products_sale = Product.objects.filter(on_sale=True)
    context = {"products_sale": products_sale}
    return render(request, "frontpage.html", context=context)


@login_required(login_url='login')
def add(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Permission Denied")
    if request.method == "POST":
        form_data = ProductForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            product = form_data.save(commit=False)
            product.user = request.user
            product.image = form_data.cleaned_data['image']
            product.save()
            return redirect("products")

    return render(request, "add.html", context={"form": ProductForm})


@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart = Cart.objects.get(customer=user)
    cart_items = cart.cart_items.all()
    cart_total_price = sum(item.product.discount_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            pincode = form.cleaned_data['pincode']
            tracking_no = "show" + str(random.randint(1000, 9999))

            # Create an order instance and save the form data
            order = Order.objects.create(
                cart=cart,
                customer=user.customer,
                fname=fname,
                lname=lname,
                email=email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                country=country,
                pincode=pincode,
                total_price=cart_total_price,
                tracking_no=tracking_no,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
            # Mark the cart as ordered
            cart.ordered = True
            cart.save()

            # Clear the cart items
            cart.cart_items.clear()

            return redirect('cart')  # Redirect to a success page after saving the form

    else:
        form = OrderForm(initial={
            'fname': user.first_name,
            'lname': user.last_name,
            'email': user.email,
        })

    context = {"cart": cart,
               "cart_items": cart_items,
               "cart_total_price": cart_total_price}
    return render(request, "order_form.html", context=context)


@login_required(login_url='login')
def createOrder(request):
    user = request.user
    cart = Cart.objects.get(customer=user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.product.discount_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = user.customer  # Retrieve the Customer instance associated with the logged-in user
            order.total_price = total_price
            order.save()

            for item in cart_items:
                item.ordered = True
                item.save()

            cart.status = 'Pending'
            cart.save()

            return redirect('cart')
    else:
        form = OrderForm()

    order_items = OrderItem.objects.filter(order__cart=cart)
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
        'order_items': order_items
    }
    return render(request, 'order_form.html', context=context)


@login_required(login_url="login")
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    cart, created = Cart.objects.get_or_create(customer=user)
    cart_item = cart.cart_items.filter(product=product).first()
    if cart_item:
        cart_item.save()
    else:
        cart_item = CartItem.objects.create(cart=cart, product=product)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_view(request):
    user = request.user
    cart = Cart.objects.get(customer=user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.product.discount_price * item.quantity for item in cart_items)

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price
    }
    return render(request, 'cart.html', context=context)


@login_required(login_url='login')
def deleteCartItem(request, pk):
    cart_item = get_object_or_404(CartItem, id=pk)
    if request.method == "POST":
        cart_item.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='login')
def order_list(request):
    user = request.user
    orders = Order.objects.filter(customer=user.customer).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'dashboard.html', context=context)
