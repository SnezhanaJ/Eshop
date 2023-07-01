from _decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    ('Laptop', 'Laptop'),
    ('Phone', 'Phone'),
    ('TV', 'TV')
)

STATUS = (
    ('Pending', 'Pending'),
    ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered')
)


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200)
    image = models.ImageField(upload_to="images/", null=True)
    screen = models.CharField(max_length=255, blank=True, null=True)
    screenSize = models.CharField(max_length=255, blank=True, null=True)
    OS = models.CharField(max_length=255, blank=True, null=True)
    memory = models.CharField(max_length=255, blank=True, null=True)
    CPU = models.CharField(max_length=255, blank=True, null=True)
    camera = models.CharField(max_length=255, blank=True, null=True)
    battery = models.CharField(max_length=255, blank=True, null=True)
    RAM = models.CharField(max_length=255, blank=True, null=True)
    on_sale = models.BooleanField(default=False, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        if self.on_sale and self.discount:
            price_decimal = Decimal(str(self.price))
            discount_amount = price_decimal * (self.discount / 100)
            return round(price_decimal - discount_amount, 2)
        else:
            return self.price


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        return CartItem.objects.filter(cart__customer=self.user).count()


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="carts")
    ordered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=200, null=True, default="Pending")

    def __str__(self):
        return f"Cart for {self.customer.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - Quantity {self.quantity}"


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    order_items = models.ManyToManyField(CartItem, related_name='orders', blank=True, null=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=200, null=True, default="Pending")
    total_price = models.FloatField(null=True, blank=True)
    tracking_no = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fname} - {self.lname} STATUS: {self.status} - {self.tracking_no}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)