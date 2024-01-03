from datetime import datetime, timedelta
from django.utils import timezone
import paypalrestsdk
from paypalrestsdk import Payment
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Subscription, UserSubscription
from django.contrib.auth.decorators import login_required

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def subscriptions_list(request):
    """
    Render a list of subscriptions.

    Args:
    - request: HttpRequest object

    Returns:
    - HttpResponse object containing rendered HTML template
    """
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions
    }
    return render(request, 'subscription/subscriptions_list.html', context)

@login_required
def subscription_detail(request, pk):
    """
    Render details of a particular subscription.

    Args:
    - request: HttpRequest object
    - pk: Primary key of the subscription

    Returns:
    - HttpResponse object containing rendered HTML template
    """
    subscription = get_object_or_404(Subscription, pk=pk)

    monthly_price = round(subscription.price, 2)
    semi_annual_price = round(monthly_price * 6 * 0.8, 2)
    annual_price = round(monthly_price * 12 * 0.65, 2)
    context = {
        'subscription': subscription,
        'monthly_price': monthly_price,
        'semi_annual_price': semi_annual_price,
        'annual_price': annual_price,
    }
    return render(request, 'subscription/subscription_detail.html', context)

@login_required
def execute_payment(request):
    """
    Execute a payment for a user subscription.

    Args:
    - request: HttpRequest object

    Returns:
    - HttpResponse indicating the status of payment execution
    """
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payer_id = request.POST.get('payer_id')
        subscription_id = request.POST.get('subscription_id')
        selected_price = request.POST.get('selected_price')

        user_subscription = get_object_or_404(UserSubscription, subscription_id=subscription_id, user=request.user)

        payment = Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            user_subscription.is_paid = True
            user_subscription.save()
            return HttpResponse("Payment successful!")
        else:
            return HttpResponse("Payment execution failed.")
    else:
        return HttpResponse("Invalid request method")

@login_required
def checkout(request):
    """
    Handle the checkout process for subscribing to a plan.

    Args:
    - request: HttpRequest object

    Returns:
    - HttpResponse object containing rendered HTML template or redirection to PayPal
    """
    if request.method == 'POST':
        subscription_id = request.POST.get('subscription_id')
        selected_duration = request.POST.get('selected_duration')
        
        if selected_duration == 'monthly':
            selected_price = request.POST.get('monthly_price')
            duration_in_days = 31
        elif selected_duration == 'semi_annual':
            selected_price = request.POST.get('semi_annual_price')
            duration_in_days = 183
        elif selected_duration == 'annual':
            selected_price = request.POST.get('annual_price')
            duration_in_days = 366
        else:
            return HttpResponse("Invalid duration selection")

        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=duration_in_days)
        
        user = request.user
        
        user_subscription = UserSubscription.objects.create(
            user=user,
            subscription_id=subscription_id,
            start_date=start_date,
            end_date=end_date
        )

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": reverse('execute_payment'),
                "cancel_url": reverse('cancel_payment')
            },
            "transactions": [{
                "amount": {
                    "total": selected_price,
                    "currency": "USD"
                },
                "description": "Subscription Payment"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return redirect(link.href)
            return HttpResponse("Failed to redirect to PayPal.")
        else:
            return HttpResponse("Payment creation failed.")
    else:
        return render(request, 'subscription/checkout.html')
