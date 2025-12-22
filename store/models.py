from django.contrib.auth.models import User
from django.db import models
import datetime
import uuid
import random
import string

STATE_CHOICES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CG', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TS', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UK', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    # Union Territories
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('JK', 'Jammu and Kashmir'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Puducherry'),
]


COUNTRY_CHOICES=[
     ('IN', 'India'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
    ('CA', 'Canada'),
    ('AU', 'Australia'),
    ('NZ', 'New Zealand'),
    ('SG', 'Singapore'),
    ('MY', 'Malaysia'),
    ('CN', 'China'),
    ('JP', 'Japan'),
    ('KR', 'South Korea'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('IT', 'Italy'),
    ('ES', 'Spain'),
    ('BR', 'Brazil'),
    ('MX', 'Mexico'),
    ('ZA', 'South Africa'),
    ('AE', 'United Arab Emirates'),
    ('SA', 'Saudi Arabia'),

]


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    product_detail = models.CharField(max_length=500, default='', blank=True, null=True)
    product_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Changed max_digits to 10
    product_img = models.ImageField(upload_to='uploads/product')
    another_product_img = models.ImageField(upload_to='uploads/product', blank=True, null=True)

    def __str__(self):
        return self.product_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=200, default='', blank=False, null=False)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default='IN', blank=False, null=False)  # Fixed: should be 'IN' not 'INDIA'
    apartment_suite = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, default='', blank=False, null=False)
    state = models.CharField(max_length=3, choices=STATE_CHOICES, default='TN', blank=False, null=False)  # Fixed: max_length should match choices
    pin_code = models.CharField(max_length=10, default='', blank=False, null=False)
 
    def __str__(self):
        return f'{self.address}, {self.city}, {self.state} {self.pin_code}'

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('razorpay', 'Razorpay'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('partial', 'Partial Payment'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer = models.CharField(max_length=100, blank=False, null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='razorpay')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    track_id = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer}"
    
    def cod_advance_amount(self):
        # 20% advance for COD
        return self.total_amount * 0.2
    
    def save(self, *args, **kwargs):
        # Import here to avoid circular imports
        import random
        import string
        
        if not self.track_id:
            length = random.choice([5, 6])
            characters = string.ascii_uppercase + string.digits
            self.track_id = ''.join(random.choice(characters) for _ in range(length))
        
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
    
    @property
    def item_total(self):
        return self.quantity * self.price
    

    def generate_track_id():
         length = random.choice([5, 6])
         characters = string.ascii_uppercase + string.digits
         return ''.join(random.choice(characters) for _ in range(length))

