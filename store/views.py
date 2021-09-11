from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .decorators import *
from .forms import UserUpdateForm, CustomerUpdateForm, ContactForm, FeedbackForm, ProductForm, OrderStatusForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .filters import ProductFilter
from django.http import JsonResponse
from django.db.models import Q
import json
import datetime


@login_required(login_url='login')
@admin_only
def admin_dashboard(request):
    customers = Customer.objects.all()
    total_customers = customers.count()

    products = Product.objects.all()
    total_products = products.count()

    orders = Order.objects.filter(complete=True)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    orders_processing = total_orders - delivered - pending

    recent_orders = Order.objects.all().exclude(complete='False')[:10]

    message = Contact.objects.filter(is_read=False).count()
    request.session['messages'] = message

    context = {'total_customers': total_customers, 'total_products': total_products, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending, 'orders_processing': orders_processing,
               'recent_orders': recent_orders}
    return render(request, 'store/admin_dashboard.html', context)


@login_required(login_url='login')
@admin_only
def admin_customer_view(request):
    customers = Customer.objects.all()

    query = request.GET.get('q')
    if query:
        customers = customers.filter(Q(user__username__icontains=query))

    context = {'customers': customers}
    return render(request, 'store/admin_view_customers.html', context)


@login_required(login_url='login')
@admin_only
def admin_customer_order_view(request):
    orders = Order.objects.all().exclude(complete='False')

    query = request.GET.get('q')
    if query:
        orders = orders.filter(Q(transaction_id=query))

    context = {'orders': orders}
    return render(request, 'store/admin_customer_order_view.html', context)


@login_required(login_url='login')
@admin_only
def admin_customer_order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderStatusForm(instance=order)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order status updated!!')
            return redirect('admin-customer-order-view')
    context = {'form': form}
    return render(request, 'store/admin_customer_order_update.html', context)


@login_required(login_url='login')
@admin_only
def admin_customer_order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.orderitem_set.all()
    address = order.shippingaddress_set.all()
    if request.method == 'POST':
        # for item in items:
        #     item.delete()
        items.delete()
        address.delete()
        order.delete()
        messages.success(request, f'Order deleted from the database!!')
        return redirect('admin-customer-order-view')
    context = {'order': order}
    return render(request, 'store/admin_customer_order_delete.html', context)


@login_required(login_url='login')
@admin_only
def admin_customer_delete(request, username):
    user = User.objects.get(username=username)
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        user.delete()
        customer.delete()
        messages.success(request, f'Customer deleted from the database!!')
        return redirect('admin-view-customer')

    context = {'customer': customer}
    return render(request, 'store/admin_delete_customer.html', context)


@login_required(login_url='login')
@admin_only
def admin_products_view(request):
    products = Product.objects.all()

    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    context = {'products': products, 'my_filter': my_filter}
    return render(request, 'store/admin_products_view.html', context)


@login_required(login_url='login')
@admin_only
def admin_product_details(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'store/admin_product_details.html', context)


@login_required(login_url='login')
@admin_only
def admin_add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('admin-product-details', pk=instance.id)
    context = {'form': form, 'section_title': 'Add Product', 'button_name': 'Add'}
    return render(request, 'store/admin_product_form.html', context)


@login_required(login_url='login')
@admin_only
def admin_update_product(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f'Product details updated!!')
            return redirect('admin-product-details', pk=instance.id)
    context = {'form': form, 'section_title': 'Update Product', 'button_name': 'Update'}
    return render(request, 'store/admin_product_form.html', context)


@login_required(login_url='login')
@admin_only
def admin_delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product deleted successfully')
        return redirect('admin-products-view')
    context = {'product': product}
    return render(request, 'store/admin_product_delete.html', context)


@login_required(login_url='login')
@admin_only
def admin_inbox(request):
    inbox = Contact.objects.all()

    request.session['messages'] = Contact.objects.filter(is_read=False).count()

    context = {'inbox': inbox}
    return render(request, 'store/admin_inbox.html', context)


@login_required(login_url='login')
@admin_only
def message_page(request, pk):
    message = Contact.objects.get(id=pk)
    message.is_read = True
    message.save()

    context = {'message': message}
    return render(request, 'store/admin_message.html', context)


@login_required(login_url='login')
@admin_only
def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created')
    context = {'feedbacks': feedbacks}
    return render(request, 'store/view_feedbacks.html', context)


@admin_restriction
def customer_products_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_cart_items = order.get_cart_items
    else:
        total_cart_items = 0

    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query)).distinct()

    # my_filter = ProductFilter(request.GET, queryset=products)
    # products = my_filter.qs

    context = {'products': products, 'total_cart_items': total_cart_items}
    return render(request, 'store/customer_products_view.html', context)


@admin_restriction
def customer_product_details(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_cart_items = order.get_cart_items
    else:
        total_cart_items = 0

    product = Product.objects.get(pk=pk)
    context = {'product': product, 'total_cart_items': total_cart_items}
    return render(request, 'store/customer_product_details.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    total_cart_items = order.get_cart_items

    if items:
        context = {'order': order, 'items': items, 'total_cart_items': total_cart_items}
        return render(request, 'store/cart.html', context)
    else:
        context = {'total_cart_items': total_cart_items}
        return render(request, 'store/empty_cart.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    total_cart_items = order.get_cart_items

    if items:
        context = {'items': items, 'order': order, 'total_cart_items': total_cart_items}
        return render(request, 'store/checkout.html', context)
    else:
        return redirect('customer-products-view')


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item added', safe=False)


def process_order(request):
    # print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        first_name=data['form']['first_name'],
        last_name=data['form']['last_name'],
        mobile=data['form']['mobile'],
        email=data['form']['email'],
        address=data['form']['address'],
        city=data['form']['city'],
        division=data['form']['division'],
    )

    return JsonResponse('Order processed', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customer_order(request):
    customer = request.user.customer

    orders = Order.objects.filter(customer=customer, complete=True)
    completed_orders = orders.filter(status='Delivered')
    running_orders = orders.exclude(status='Delivered')

    total_orders = orders.count()
    delivered = completed_orders.count()
    pending = orders.filter(status='Pending').count()
    orders_processing = total_orders - delivered - pending

    context = {'completed_orders': completed_orders, 'running_orders': running_orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending, 'orders_processing': orders_processing}
    return render(request, 'store/customer_orders.html', context)


@login_required(login_url='login')
def profile(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total_cart_items = order.get_cart_items
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        customer_update_form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        if user_update_form.is_valid() or customer_update_form.is_valid():
            user_update_form.save()
            customer_update_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        customer_update_form = CustomerUpdateForm(instance=request.user.customer)

    context = {'user_update_form': user_update_form, 'customer_update_form': customer_update_form,
               'total_cart_items': total_cart_items}
    return render(request, 'store/profile.html', context)


@admin_restriction
def send_feedback(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_cart_items = order.get_cart_items
    else:
        total_cart_items = 0
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Thanks for your valuable feedback!')
            return redirect('send-feedback')
    context = {'form': form, 'total_cart_items': total_cart_items}
    return render(request, 'store/send_feedback.html', context)


@admin_restriction
def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_cart_items = order.get_cart_items
    else:
        total_cart_items = 0
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Thanks for contacting. I'll try to contact you back as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()
    context = {'form': form, 'total_cart_items': total_cart_items}
    return render(request, 'store/contact.html', context)


@admin_restriction
def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_cart_items = order.get_cart_items
    else:
        total_cart_items = 0
    context = {'total_cart_items': total_cart_items}
    return render(request, 'store/about.html', context)
