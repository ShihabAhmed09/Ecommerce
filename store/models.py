from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    mobile = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(default='users/blank-profile-picture.png', upload_to='users')

    def __str__(self):
        return f'{self.user}'

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='store', default='store/placeholder.png', null=True, blank=True)
    tags = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ['tags', 'name']


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(default=timezone.now, null=True)
    status = models.CharField(choices=STATUS, default='Pending', max_length=200, null=True)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.customer}'

    @property
    def get_cart_total(self):  # calculates overall total price
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):  # calculates overall total items
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    class Meta:
        ordering = ['-date_ordered']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):  # calculates individual total price
        total = self.product.price * self.quantity
        return total

    class Meta:
        ordering = ['-date_added']


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    division = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, {self.email} at {self.created}'

    class Meta:
        ordering = ['is_read', '-created']


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    feedback = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
