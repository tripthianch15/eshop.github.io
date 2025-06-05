from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Payment
from django.utils import timezone
import uuid
from products.models import Cart
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
import razorpay
from datetime import datetime

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required
def initiate_payment(request):
    orders = Order.objects.filter(buyer=request.user)
    payment = Payment.objects.create(amount=0, user=request.user, payment_status='Initiated')

    for order in orders:
        payment.orders.add(order)
        payment.amount += order.total_amount
        

    payment.save()
    currency = 'INR'
    razorpay_amount = int(float(payment.amount) * 100)  # Convert to paise

    notes = f'Transaction number: {payment.transaction_id}  ({request.user.first_name}), {request.user.contact_number}'

    order_data = {
        'amount': razorpay_amount,
        'currency': currency,
        'receipt': payment.transaction_id,
        'payment_capture': '0',
        'notes': {'note_key': notes}
    }

    razorpay_order = razorpay_client.order.create(order_data)
    request.session['transaction_id'] = payment.transaction_id

    context = {
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_amount': razorpay_amount,
        'amount': payment.amount,
        'currency': currency,
        'callback_url': '/paymenthandler/',
    }

    return render(request, 'payments/payment.html', context)


@csrf_exempt
def paymenthandler(request):
    try:
        transaction_id = request.session.get('transaction_id')
        if not transaction_id:
            return HttpResponseBadRequest("Missing transaction ID.")

        payment = get_object_or_404(Payment, transaction_id=transaction_id)
        razorpay_amount = int(float(payment.amount) * 100)  # Convert to paise

        if request.method == "POST":
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            print("payment_id: ", razorpay_payment_id)
            print("\n razorpay_order_id: ",razorpay_order_id)
            print("\n Transaction id: ", transaction_id)
            print("\nAmount: ", razorpay_amount)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': signature
            }

            # Verify the signature
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                razorpay_client.payment.capture(razorpay_payment_id, razorpay_amount)

                # Get transaction details
                payment_details = razorpay_client.payment.fetch(razorpay_payment_id)
                contact = payment_details.get('contact', '')
                method = payment_details.get('method', '')
                created_at_timestamp = payment_details.get('created_at')
                payment_date = timezone.make_aware(datetime.fromtimestamp(created_at_timestamp))

                payment.transaction_id = transaction_id
                payment.payment_status = 'Completed'
                payment.payment_date = payment_date
                payment.gw_order_id = razorpay_order_id
                payment.gw_payment_id = razorpay_payment_id
                payment.gw_response = f"Signature: {signature}"
                payment.description = (
                    f"Customer: {contact}, Method: {method}, Created At: {payment_date}, "
                    f"Signature: {signature}, Details: {payment_details}"
                )
                payment.save()

                # Update orders
                for order in payment.orders.all():
                    order.status = 'Shipping'
                    order.is_deleted = 'N'
                    order.transaction_id = payment.transaction_id
                    order.save()

                # Clear cart
                cart = Cart.objects.filter(user=request.user).first()
                if cart:
                    cart.delete()

                messages.success(request, "Payment successful!")
                return redirect('order_confirmation')

            except razorpay.errors.SignatureVerificationError:
                payment.payment_status = 'Failed'
                payment.save()
                return HttpResponse("Signature verification failed.", status=400)

        return HttpResponseBadRequest("Invalid request method.")

    except Payment.DoesNotExist:
        return HttpResponse("Invalid transaction.", status=400)

    except Exception as e:
        return HttpResponse(f"Error occurred: {str(e)}", status=500)


@login_required
def process_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    if request.method == "POST":
        payment.payment_status = 'Completed'
        payment.payment_date = timezone.now()
        payment.save()

        for order in payment.orders.all():
            order.status = 'Shipping'
            order.save()

        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.delete()

        messages.success(request, "Your payment was successful!")
        return redirect('order_confirmation')

    return render(request, 'payments/process_payment.html', {'payment': payment})
