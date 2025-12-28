# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import *
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# import json
# from decimal import Decimal
# from django.contrib.auth.decorators import user_passes_test
# from django.db.models import Count, Sum
# from datetime import datetime, timedelta
# import traceback
# from django.utils import timezone
# import csv
# import random
# import string
# from django.contrib import messages
# import hashlib
# from functools import wraps

# def home(request):
#     products = Products.objects.all()
#     return render(request, 'homepage.html', {'products': products})

# def product(request, product_id):
#     product = get_object_or_404(Products, id=product_id)
#     return render(request, 'product.html', {'product': product})

# def about(request):
#     return render(request,'about_us.html')

# def contact(request):
#     return render(request,'contact.html')

# def cart(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     subtotal = Decimal('0')
#     total_items = 0
    
#     for product_id, item_data in cart.items():
#         try:
#             product = Products.objects.get(id=item_data['product_id'])
#             quantity = item_data.get('quantity', 1)
            
#             # Get price
#             if 'price_decimal' in item_data:
#                 price = Decimal(str(item_data['price_decimal']))
#             else:
#                 try:
#                     price = Decimal(str(item_data['price']))
#                 except (ValueError, TypeError):
#                     price = product.product_price
            
#             item_total = price * quantity
#             subtotal += item_total
#             total_items += quantity
            
#             cart_items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'price': price,
#                 'item_total': item_total,
#                 'name': item_data.get('name', product.product_name),
#                 'image': item_data.get('image', ''),
#                 'subtitle': item_data.get('subtitle', '')
#             })
#         except Products.DoesNotExist:
#             continue
    
#     total = subtotal
    
#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'total': total,
#         'total_items': total_items,
#     }
#     return render(request, 'cart.html', context)



# def add_to_cart(request):
#     if request.method != 'POST':
#         return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

#     product_id = request.POST.get('productid')
    
#     try:
#         quantity = int(request.POST.get('quantity', 1))
#     except (ValueError, TypeError):
#         quantity = 1

#     try:
#         product = Products.objects.get(id=product_id)
#     except Products.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

#     # Initialize cart from session
#     cart = request.session.get('cart', {})
#     product_id_str = str(product_id)

#     if product_id_str in cart:
#         cart[product_id_str]['quantity'] += quantity
#     else:
#         cart[product_id_str] = {
#             'product_id': product.id,
#             'name': product.product_name,
#             'price': float(product.product_price),
#             'image': product.product_img_url or '',
#             'quantity': quantity,
#             'subtitle': product.product_detail[:50] if product.product_detail else ''
#         }

#     request.session['cart'] = cart
#     request.session.modified = True

#     total_items = sum(item['quantity'] for item in cart.values())

#     return redirect("cart") 

  
        
        

# def update_cart_item(request, product_id):
#     if request.method == 'POST':
#         try:
#             cart = request.session.get('cart', {})
#             product_id_str = str(product_id)
            
#             data = json.loads(request.body)
#             quantity = int(data.get('quantity', 1))
            
#             if product_id_str in cart:
#                 if quantity > 0:
#                     cart[product_id_str]['quantity'] = quantity
#                     message = "Cart updated successfully"
#                 else:
#                     del cart[product_id_str]
#                     message = "Item removed from cart"
                
#                 request.session['cart'] = cart
#                 request.session.modified = True
                
#                 subtotal = 0
#                 total_items = 0
                
#                 for pid_str, item_data in cart.items():
#                     try:
#                         product = Products.objects.get(id=item_data['product_id'])
#                         qty = item_data['quantity']
#                         price = float(item_data['price'])
#                         subtotal += price * qty
#                         total_items += qty
#                     except (Products.DoesNotExist, KeyError):
#                         continue
                
#                 total = subtotal
                
#                 return JsonResponse({
#                     'success': True,
#                     'message': message,
#                     'item_price': float(price) * quantity if quantity > 0 else 0,
#                     'cart_data': {
#                         'subtotal': float(subtotal),
#                         'total': float(total),
#                         'total_items': total_items
#                     }
#                 })
#             else:
#                 return JsonResponse({'success': False, 'error': 'Item not in cart'})
                
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
    
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def remove_from_cart(request, product_id):
#     if request.method == 'POST':
#         cart = request.session.get('cart', {})
#         product_id_str = str(product_id)
        
#         if product_id_str in cart:
#             del cart[product_id_str]
#             request.session['cart'] = cart
#             request.session.modified = True
            
#             subtotal = 0
#             total_items = 0
            
#             for pid_str, item_data in cart.items():
#                 try:
#                     product = Products.objects.get(id=item_data['product_id'])
#                     qty = item_data['quantity']
#                     price = float(item_data['price'])
#                     subtotal += price * qty
#                     total_items += qty
#                 except (Products.DoesNotExist, KeyError):
#                     continue
            
#             total = subtotal
            
#             return JsonResponse({
#                 'success': True,
#                 'message': 'Product removed from cart',
#                 'cart_data': {
#                     'subtotal': float(subtotal),
#                     'total': float(total),
#                     'total_items': total_items
#                 }
#             })
#         else:
#             return JsonResponse({'success': False, 'error': 'Product not in cart'})
    
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def get_cart_count(request):
#     cart = request.session.get('cart', {})
#     count = sum(item['quantity'] for item in cart.values())
#     return JsonResponse({'success': True, 'count': count})

# def clear_cart(request):
#     if request.method == 'POST':
#         if 'cart' in request.session:
#             del request.session['cart']
#             request.session.modified = True
#         return JsonResponse({'success': True, 'message': 'Cart cleared'})
    
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def buy_now(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('productid')
#         quantity = int(request.POST.get('quantity', 1))

#         product = get_object_or_404(Products, id=product_id)

#         # CLEAR old cart first
#         request.session['cart'] = {}

#         request.session['cart'][str(product_id)] = {
#             'product_id': product.id,
#             'name': product.product_name,
#             'price': float(product.product_price),
#             'image': product.product_img_url or '',
#             'quantity': quantity,
#             'subtitle': product.product_detail[:50] if product.product_detail else ''
#         }

#         request.session.modified = True
#         return redirect('checkout')


# def generate_track_id():
#     """Generate a random 5-6 digit alphanumeric track ID"""
#     length = random.choice([5, 6])
#     characters = string.ascii_uppercase + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))


# def checkout(request):
#     # GET request - show checkout page
#     cart = request.session.get('cart', {})
#     cart_items = []
#     subtotal = 0
#     total_items = 0
    
#     for product_id_str, item_data in cart.items():
#         try:
#             product = Products.objects.get(id=item_data['product_id'])
#             price = float(item_data['price'])
#             quantity = item_data['quantity']
#             item_total = price * quantity
#             subtotal += item_total
#             total_items += quantity
            
#             cart_items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'price': price,
#                 'item_total': item_total,
#                 'name': item_data['name']
#             })
#         except Products.DoesNotExist:
#             continue
    
#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'total': subtotal,
#         'total_items': total_items,
#         'state_choices': STATE_CHOICES,
#         'country_choices': COUNTRY_CHOICES,
#     }
    
#     if request.method == 'POST':
#         try:
#             data = request.POST
            
#             customer = data.get('customer')
#             phone = data.get('phone')
#             email = data.get('email')
#             address_line = data.get('address')
#             apartment_suite = data.get('apartment_suite', '')
#             city = data.get('city')
#             state = data.get('state')
#             country = data.get('country')
#             pin_code = data.get('pin_code')
#             notes = data.get('notes', '')
#             payment_method = data.get('payment_method', 'razorpay')
            
#             errors = {}
#             if not customer:
#                 errors['customer'] = ['Full name is required']
#             if not phone or len(phone) != 10:
#                 errors['phone'] = ['Valid 10-digit phone number is required']
#             if not email:
#                 errors['email'] = ['Email is required']
#             if not address_line:
#                 errors['address'] = ['Address is required']
#             if not city:
#                 errors['city'] = ['City is required']
#             if not pin_code or len(pin_code) != 6:
#                 errors['pin_code'] = ['Valid 6-digit pin code is required']
#             if not state:
#                 errors['state'] = ['State is required']
#             if not country:
#                 errors['country'] = ['Country is required']
            
#             if errors:
#                 return JsonResponse({'success': False, 'errors': errors})
            
#             cart = request.session.get('cart', {})
#             if not cart:
#                 return JsonResponse({'success': False, 'error': 'Your cart is empty'})
            
#             total_amount = 0
#             for item in cart.values():
#                 total_amount += float(item['price']) * item['quantity']
            
#             shipping_address = Address.objects.create(
#                 user=None,
#                 address=address_line,
#                 apartment_suite=apartment_suite,
#                 city=city,
#                 state=state,
#                 country=country,
#                 pin_code=pin_code
#             )
            
#             # Generate track ID
#             track_id = generate_track_id()
            
#             # Create order
#             order = Order.objects.create(
#                 user=None,
#                 customer=customer,
#                 phone=phone,
#                 email=email,
#                 address=shipping_address,
#                 total_amount=total_amount,
#                 payment_method=payment_method,
#                 notes=notes,
#                 status='pending',
#                 payment_status='pending',
#                 track_id=track_id
#             )
            
#             for product_id_str, item_data in cart.items():
#                 try:
#                     product = Products.objects.get(id=item_data['product_id'])
#                     OrderItem.objects.create(
#                         order=order,
#                         product=product,
#                         quantity=item_data['quantity'],
#                         price=item_data['price']
#                     )
#                 except Products.DoesNotExist:
#                     continue
            
#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
#             if payment_method == 'razorpay':
#                 razorpay_order = client.order.create({
#                     'amount': int(total_amount * 100),
#                     'currency': 'INR',
#                     'payment_capture': 1,
#                     'notes': {
#                         'order_id': str(order.id),
#                         'order_uuid': str(order.order_id)
#                     }
#                 })
                
#                 order.razorpay_order_id = razorpay_order['id']
#                 order.save()
                
#                 return JsonResponse({
#                     'success': True,
#                     'payment_method': 'razorpay',
#                     'razorpay_key': settings.RAZORPAY_KEY_ID,
#                     'amount': int(total_amount * 100),
#                     'razorpay_order_id': razorpay_order['id'],
#                     'order_id': order.id,
#                     'order_uuid': str(order.order_id)
#                 })
                
#             elif payment_method == 'cod':
#                 advance_amount = total_amount * 0.2
                
#                 razorpay_order = client.order.create({
#                     'amount': int(advance_amount * 100),
#                     'currency': 'INR',
#                     'payment_capture': 1,
#                     'notes': {
#                         'order_id': str(order.id),
#                         'order_uuid': str(order.order_id),
#                         'is_cod_advance': 'true'
#                     }
#                 })
                
#                 order.razorpay_order_id = razorpay_order['id']
#                 order.save()
                
#                 return JsonResponse({
#                     'success': True,
#                     'payment_method': 'cod',
#                     'razorpay_key': settings.RAZORPAY_KEY_ID,
#                     'amount': int(advance_amount * 100),
#                     'razorpay_order_id': razorpay_order['id'],
#                     'order_id': order.id,
#                     'order_uuid': str(order.order_id)
#                 })
                
#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({'success': False, 'error': str(e)})
    
#     return render(request, 'checkout.html', context)

# @csrf_exempt

# @csrf_exempt
# def verify_payment(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             order_id = int(data.get('order_id'))  # make sure it's int

#             order = Order.objects.get(id=order_id)

#             client = razorpay.Client(
#                 auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#             )

#             params_dict = {
#                 'razorpay_order_id': data['razorpay_order_id'],
#                 'razorpay_payment_id': data['razorpay_payment_id'],
#                 'razorpay_signature': data['razorpay_signature'],
#             }

#             client.utility.verify_payment_signature(params_dict)

#             order.razorpay_payment_id = data['razorpay_payment_id']
#             order.razorpay_signature = data['razorpay_signature']

#             # if order.payment_method == 'cod':
#             #     order.payment_status = 'partial'
#             #     order.status = 'processing'
#             #     message = '20% advance paid. COD order confirmed.'

#             if order.payment_status in ['completed', 'partial']:
#                 return JsonResponse({
#         'success': True,
#         'redirect_url': f'/order-success/{order.id}/'
#     })

#             else:
#                 order.payment_status = 'completed'
#                 order.status = 'processing'
#                 message = 'Payment successful. Order confirmed.'

#             order.save()

#             # clear cart
#             request.session.pop('cart', None)

#             return JsonResponse({
#                 'success': True,
#                 'message': message,
#                 'redirect_url': f'/order-success/{order.id}/'
#             })

#         except razorpay.errors.SignatureVerificationError:
#             return JsonResponse({'success': False, 'error': 'Payment verification failed'})

#         except Order.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Order not found'})

#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Invalid request'})


# def order_success(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = order.items.all()

#     cod_advance = 0
#     balance_on_delivery = 0

#     if order.payment_method == 'cod' and order.payment_status == 'partial':
#         total = float(order.total_amount)
#         cod_advance = total * 0.2
#         balance_on_delivery = total * 0.8

#     return render(request, 'order_success.html', {
#         'order': order,
#         'track_id': order.track_id,
#         'cod_advance': cod_advance,
#         'balance_on_delivery': balance_on_delivery,
#         'order_items': order_items,
#     })



# def is_admin(user):
#     return user.is_superuser or user.is_staff

# ADMIN_PASSWORD = "vi.jix@25#11"

# def admin_password_required(view_func):
#     """
#     Decorator that requires admin password to access certain views
#     """
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         # Check if password is already verified in session
#         if request.session.get('admin_authenticated') == True:
#             return view_func(request, *args, **kwargs)
        
#         # If POST request with password
#         if request.method == 'POST':
#             password = request.POST.get('admin_password', '')
#             if password == ADMIN_PASSWORD:
#                 # Set session variable
#                 request.session['admin_authenticated'] = True
#                 # Session expires in 8 hours
#                 request.session.set_expiry(28800)
#                 return view_func(request, *args, **kwargs)
#             else:
#                 messages.error(request, 'Invalid password!')
#                 return redirect('admin_login')
        
#         # If not authenticated and not POST, redirect to password page
#         return redirect('admin_login')
    
#     return _wrapped_view

# @admin_password_required 
# def admin_dashboard(request):
#     today = datetime.now().date()
#     week_ago = today - timedelta(days=7)
#     month_ago = today - timedelta(days=30)
    
#     all_orders = Order.objects.all().order_by('-created_at')
    
#     total_orders = all_orders.count()
#     total_revenue = all_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
#     today_orders = all_orders.filter(created_at__date=today).count()
#     week_orders = all_orders.filter(created_at__date__gte=week_ago).count()
#     month_orders = all_orders.filter(created_at__date__gte=month_ago).count()
    
#     payment_stats = all_orders.values('payment_method').annotate(
#         count=Count('id'),
#         total=Sum('total_amount')
#     )
    
#     status_stats = all_orders.values('status').annotate(
#         count=Count('id')
#     )
    
#     recent_orders = all_orders[:10]
    
#     context = {
#         'orders': all_orders,
#         'recent_orders': recent_orders,
#         'stats': {
#             'total_orders': total_orders,
#             'total_revenue': total_revenue,
#             'today_orders': today_orders,
#             'week_orders': week_orders,
#             'month_orders': month_orders,
#             'payment_stats': payment_stats,
#             'status_stats': status_stats,
#         }
#     }
#     return render(request, 'admin_dashboard.html', context)

# @login_required
# @user_passes_test(is_admin)
# def order_detail_admin(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         order_items = OrderItem.objects.filter(order=order)
        
#         cod_advance = None
#         balance_due = None
#         if order.payment_method == 'cod' and order.payment_status == 'partial':
#             cod_advance = float(order.total_amount) * 0.2
#             balance_due = float(order.total_amount) - cod_advance
        
#         context = {
#             'order': order,
#             'track_id': order.track_id,
#             'order_items': order_items,
#             'cod_advance': cod_advance,
#             'balance_due': balance_due,
#         }
#         return render(request, 'admin_order_detail.html', context)
        
#     except Order.DoesNotExist:
#         return redirect('admin_dashboard')

# def order_details(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         order_items = OrderItem.objects.filter(order=order)
        
#         cod_advance = None
#         balance_due = None
#         if order.payment_method == 'cod' and order.payment_status == 'partial':
#             cod_advance = float(order.total_amount) * 0.2
#             balance_due = float(order.total_amount) - cod_advance
        
#         context = {
#             'order': order,
#             'track_id': order.track_id,
#             'order_items': order_items,
#             'cod_advance': cod_advance,
#             'balance_due': balance_due,
#         }
#         return render(request, 'order_detail.html', context)
        
#     except Order.DoesNotExist:
#         return redirect('home')

# def print_shipping_label(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
    
#     try:
#         total_items = sum(item.quantity for item in order.items.all())
#     except:
#         total_items = 0
    
#     context = {
#         'order': order,
#         'track_id': order.track_id,
#         'total_items': total_items,
#     }
    
#     return render(request, 'shipping_label.html', context)

# def bulk_print_shipping_labels(request):
#     order_ids = request.GET.get('orders', '').split(',')
#     orders = Order.objects.filter(id__in=order_ids)
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'bulk_shipping_labels.html', context)

# def print_today_orders(request):
#     today = timezone.now().date()
#     orders = Order.objects.filter(created_at__date=today)
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'bulk_shipping_labels.html', context)

# def print_all_orders(request):
#     orders = Order.objects.all()
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'bulk_shipping_labels.html', context)

# def print_pending_orders(request):
#     orders = Order.objects.filter(status='pending')
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'bulk_shipping_labels.html', context)

# def print_cod_orders(request):
#     orders = Order.objects.filter(payment_method='cod')
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'bulk_shipping_labels.html', context)

# @csrf_exempt
# def delete_order(request, order_id):
#     if request.method == 'POST':
#         try:
#             order = Order.objects.get(id=order_id)
#             order.delete()
#             return JsonResponse({'success': True, 'message': 'Order deleted successfully'})
#         except Order.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Order not found'})
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# @csrf_exempt
# def delete_orders(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             order_ids = data.get('order_ids', [])
#             Order.objects.filter(id__in=order_ids).delete()
#             return JsonResponse({'success': True, 'message': f'{len(order_ids)} orders deleted'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

# def print_orders_by_date(request):
#     date_str = request.GET.get('date')
#     try:
#         date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         orders = Order.objects.filter(created_at__date=date)
#     except:
#         orders = Order.objects.filter(created_at__date=datetime.today().date())
    
#     context = {'orders': orders}
#     return render(request, 'bulk_shipping_labels.html', context)

# def print_all_labels(request):
#     orders = Order.objects.all()
#     context = {'orders': orders}
#     return render(request, 'bulk_shipping_labels.html', context)

# def export_orders(request):
#     order_ids = request.GET.get('orders', '').split(',')
#     orders = Order.objects.filter(id__in=order_ids)
    
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'
    
#     writer = csv.writer(response)
#     writer.writerow(['Order ID', 'Customer', 'Date', 'Amount', 'Payment Method', 'Status', 'Phone', 'Email', 'Track ID'])
    
#     for order in orders:
#         writer.writerow([
#             order.order_id,
#             order.customer,
#             order.created_at.strftime('%Y-%m-%d'),
#             order.total_amount,
#             order.get_payment_method_display(),
#             order.get_status_display(),
#             order.phone,
#             order.email,
#             order.track_id
#         ])
    
#     return response





# # Add this view function to views.py
# def admin_login(request):
#     """
#     Admin password login page
#     """
#     # If already authenticated, redirect to dashboard
#     if request.session.get('admin_authenticated'):
#         return redirect('admin_dashboard')
    
#     # Handle password submission
#     if request.method == 'POST':
#         password = request.POST.get('admin_password', '')
#         if password == ADMIN_PASSWORD:
#             request.session['admin_authenticated'] = True
#             request.session.set_expiry(28800)  # 8 hours
#             return redirect('admin_dashboard')
#         else:
#             messages.error(request, 'Invalid password!')
    
#     return render(request, 'admin_login.html')


# # Add this view function to views.py
# def admin_login(request):
#     """
#     Admin password login page
#     """
#     # If already authenticated, redirect to dashboard
#     if request.session.get('admin_authenticated'):
#         return redirect('admin_dashboard')
    
#     # Handle password submission
#     if request.method == 'POST':
#         password = request.POST.get('admin_password', '')
#         if password == ADMIN_PASSWORD:
#             request.session['admin_authenticated'] = True
#             request.session.set_expiry(28800)  # 8 hours
#             return redirect('admin_dashboard')
#         else:
#             messages.error(request, 'Invalid password!')
    
#     return render(request, 'admin_login.html')


from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import razorpay
import json
import random
import string

from .models import *


# -------------------------
# BASIC PAGES
# -------------------------

def home(request):
    products = Products.objects.all()
    return render(request, 'homepage.html', {'products': products})


def product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'product.html', {'product': product})


def about(request):
    return render(request, 'about_us.html')


def contact(request):
    return render(request, 'contact.html')


# -------------------------
# CART
# -------------------------

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0')
    total_items = 0

    for item in cart.values():
        product = get_object_or_404(Products, id=item['product_id'])
        qty = item['quantity']
        price = Decimal(str(item['price']))
        item_total = price * qty

        subtotal += item_total
        total_items += qty

        cart_items.append({
            'product': product,
            'quantity': qty,
            'price': price,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': subtotal,
        'total_items': total_items
    })


def add_to_cart(request):
    if request.method != 'POST':
        return redirect('cart')

    product_id = request.POST.get('productid')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Products, id=product_id)

    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += quantity
    else:
        cart[pid] = {
            'product_id': product.id,
            'name': product.product_name,
            'price': float(product.product_price),
            'image': product.product_img_url or '',
            'quantity': quantity,
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


def clear_cart(request):
    request.session.pop('cart', None)
    return redirect('cart')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': count})


def buy_now(request):
    if request.method != 'POST':
        return redirect('home')

    product_id = request.POST.get('productid')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Products, id=product_id)

    request.session['cart'] = {
        str(product_id): {
            'product_id': product.id,
            'name': product.product_name,
            'price': float(product.product_price),
            'quantity': quantity,
        }
    }

    return redirect('checkout')


# -------------------------
# BUY NOW
# -------------------------

from django.utils import timezone
from decimal import Decimal

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    subtotal = Decimal('0')

    for item in cart.values():
        price = Decimal(str(item['price']))
        qty = item['quantity']
        item_total = price * qty
        subtotal += item_total

        cart_items.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': price,
            'quantity': qty,
            'item_total': item_total
        })

    total = subtotal  # free shipping

    # ----------------------------
    # GET → SHOW CHECKOUT PAGE
    # ----------------------------
    if request.method == 'GET':
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'total': total,
            'state_choices': STATE_CHOICES,     # ✅ FROM MODELS
            'country_choices': COUNTRY_CHOICES, # ✅ FROM MODELS
            'current_date': timezone.now().date(),
        })

    # ----------------------------
    # POST → CREATE ORDER
    # ----------------------------
    data = request.POST
    payment_method = data.get('payment_method')

    address = Address.objects.create(
        address=data.get('address'),
        apartment_suite=data.get('apartment_suite', ''),
        city=data.get('city'),
        state=data.get('state'),
        country=data.get('country'),
        pin_code=data.get('pin_code'),
    )

    order = Order.objects.create(
        customer=data.get('customer'),
        phone=data.get('phone'),
        email=data.get('email'),
        address=address,
        total_amount=total,
        payment_method=payment_method,
        payment_status='pending'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )

    # Razorpay
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payable_amount = total
    if payment_method == 'cod':
        payable_amount = total * Decimal('0.2')

    razorpay_order = client.order.create({
        'amount': int(payable_amount * 100),
        'currency': 'INR',
        'payment_capture': 1
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return JsonResponse({
        'success': True,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'amount': int(payable_amount * 100),
        'order_id': order.id,
        'payment_method': payment_method
    })



# -------------------------
# PAYMENT VERIFY
# -------------------------

@csrf_exempt
def verify_payment(request):
    data = json.loads(request.body)

    order = get_object_or_404(Order, id=data['order_id'])
    order.payment_status = 'paid'
    order.save()

    request.session.pop('cart', None)

    return JsonResponse({
        'success': True,
        'redirect_url': f'/order-success/{order.id}/'
    })


# -------------------------
# ORDER SUCCESS
# -------------------------

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


# -------------------------
# SIMPLE ADMIN (NO DJANGO LOGIN)
# -------------------------

ADMIN_PASSWORD = "vi.jix@25#11"


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_authenticated'):
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login(request):
    if request.method == 'POST':
        if request.POST.get('admin_password') == ADMIN_PASSWORD:
            request.session['admin_authenticated'] = True
            return redirect('admin_dashboard')
        messages.error(request, 'Wrong password')
    return render(request, 'admin_login.html')


from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Order


@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    # ✅ ONLY SUCCESSFUL PAYMENTS
    successful_orders = Order.objects.filter(payment_status='completed')

    # =========================
    # STATISTICS
    # =========================

    total_revenue = successful_orders.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_orders = Order.objects.count()

    today_orders = Order.objects.filter(
        created_at__date=today
    ).count()

    month_orders = Order.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month
    ).count()

    pending_orders = Order.objects.filter(status='pending').count()
    cod_orders = Order.objects.filter(payment_method='cod').count()

    # =========================
    # PAYMENT METHOD STATS (ONLY COMPLETED)
    # =========================
    payment_stats = successful_orders.values(
        'payment_method'
    ).annotate(
        count=Count('id'),
        total=Sum('total_amount')
    )

    # =========================
    # ORDER STATUS STATS
    # =========================
    status_stats = Order.objects.values(
        'status'
    ).annotate(
        count=Count('id')
    )

    # =========================
    # RECENT ORDERS
    # =========================
    recent_orders = Order.objects.order_by('-created_at')[:50]

    context = {
        'stats': {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'today_orders': today_orders,
            'month_orders': month_orders,
            'pending_orders': pending_orders,
            'cod_orders': cod_orders,
            'payment_stats': payment_stats,
            'status_stats': status_stats,
        },
        'recent_orders': recent_orders,
    }

    return render(request, 'admin_dashboard.html', context)



@admin_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Get all items for this order
    order_items_queryset = OrderItem.objects.filter(order=order)
    
    # Prepare order_items as a list of dicts
    order_items = []
    for item in order_items_queryset:
        product = item.product  # Assuming OrderItem has a ForeignKey to Products
        order_items.append({
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item.quantity * item.price,
        })
    
    # For COD calculations
    cod_advance = 0
    balance_due = 0
    if order.payment_method == 'cod' and order.payment_status == 'partial':
        cod_advance = float(order.total_amount) * 0.2
        balance_due = float(order.total_amount) - cod_advance
    
    context = {
        'order': order,
        'order_items': order_items,
        'cod_advance': cod_advance,
        'balance_due': balance_due
    }
    
    # Only one return
    return render(request, 'admin_order_detail.html', context)



def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


def print_shipping_label(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # use PK instead
    balance_amount = 0
    if order.payment_method == 'cod' and order.payment_status == 'partial':
        balance_amount = order.total_amount - order.paid_amount
    return render(request, 'shipping_label.html', {
        'order': order,
        'balance_amount': balance_amount,
        'total_items': order.items.count(),
    })



# store/views.py
from django.shortcuts import render
from .models import Order

def print_all_orders(request):
    orders = Order.objects.all()  # Or filter as needed
    return render(request, 'bulk_shipping_labels.html', {'orders': orders})


from django.shortcuts import render
from store.models import Order
from django.utils.dateparse import parse_date

def print_orders_by_date(request):
    date_str = request.GET.get('date')
    if date_str:
        date_obj = parse_date(date_str)  # converts string "YYYY-MM-DD" to date
        if date_obj:
            orders = Order.objects.filter(created_at__date=date_obj)
        else:
            orders = Order.objects.none()
    else:
        orders = Order.objects.none()

    return render(request, 'bulk_shipping_labels.html', {'orders': orders})

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Get all items for this order
    order_items_queryset = OrderItem.objects.filter(order=order)
    
    # Prepare order_items as a list of dicts
    order_items = []
    for item in order_items_queryset:
        product = item.product  # Assuming OrderItem has a ForeignKey to Products
        order_items.append({
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'item_total': item.quantity * item.price,
        })
    
    # For COD calculations
    cod_advance = 0
    balance_due = 0
    if order.payment_method == 'cod' and order.payment_status == 'partial':
        cod_advance = float(order.total_amount) * 0.2
        balance_due = float(order.total_amount) - cod_advance
    
    context = {
        'order': order,
        'order_items': order_items,
        'cod_advance': cod_advance,
        'balance_due': balance_due
    }
    return render(request, 'order_details.html', context)
