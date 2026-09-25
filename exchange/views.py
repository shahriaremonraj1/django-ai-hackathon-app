from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DepositForm, UserRegisterForm
from .models import Profile, Transaction


def register_view(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      Profile.objects.create(user=user)
      login(request, user)
      return redirect('dashboard')
  else:
    form = UserRegisterForm()
  return render(request, 'exchange/register.html', {'form': form})


@login_required
def dashboard_view(request):
  profile, created = Profile.objects.get_or_create(user=request.user)
  if request.method == 'POST':
    action = request.POST.get('action')
    amount = float(request.POST.get('amount', 0))

    if action == 'buy' and profile.balance_usd >= amount:
      profile.balance_usd -= amount
      profile.save()
    elif action == 'sell':
      profile.balance_usd += amount
      profile.save()
    return redirect('dashboard')

  return render(request, 'exchange/dashboard.html', {'profile': profile})


@login_required
def deposit_view(request):
  if request.method == 'POST':
    form = DepositForm(request.POST)
    if form.is_valid():
      tx = form.save(commit=False)
      tx.user = request.user
      tx.tx_type = 'Deposit'
      tx.save()
      profile = request.user.profile
      profile.balance_bdt += tx.amount
      profile.save()
      return redirect('dashboard')
  else:
    form = DepositForm()
  return render(request, 'exchange/deposit.html', {'form': form})