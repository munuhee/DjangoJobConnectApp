from django.shortcuts import render
from django.http import JsonResponse
import json
from users.models import Profile
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

def simpleCheckout(request, pk):
    context = {'userplan':userplan}
    return render(request, 'memberships/plans.html')
def plan(request):
    plans = Plan.objects.all()
    context = {'plans':plans}
    return render(request, 'memberships/homeplan.html', context)

@login_required(login_url='login')
def checkout(request, pk):
    plan = Plan.objects.get(id=pk)
    context = {'plan':plan}
    return render(request, 'memberships/checkout.html', context)

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    user = User.objects.get(id=body['userId'])
    plan = Plan.objects.get(id=body['planId'])
    UserPlan.objects.create(
        plan=plan,
        user=user
    )
    return JsonResponse('Payment Completed', safe=False)
