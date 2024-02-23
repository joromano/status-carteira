from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .api_handler import *
import datetime
from dateutil.relativedelta import relativedelta
import json
from decimal import Decimal

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
    return render(request, 'app/login.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def index(request):
    user = request.user
    wallets = Wallet.objects.filter(user=user, active=True)
    entries = []
    position = 0
    current_position = 0
    revenue = 0

    historical_x = []
    historical_position = []
    historical_current_position = []

    
    for wallet in wallets:
        current_price = get_current_price(wallet.ticker)
        # Create list of current stock
        entries.append({'ticker': wallet.ticker, 'date': wallet.date, 'price': wallet.price, 'qtd': wallet.qtd, 'current_price': current_price, 'id': wallet.id})

        # Calculate positions
        position += wallet.qtd * wallet.price
        current_position += wallet.qtd * Decimal(current_price)
        revenue = current_position - position

    # Calculate historical position
    # generate list of all weekdays since 3 months ago
    weekdays = []
    today = datetime.date.today()

    current_date = today
    while current_date >= datetime.date.today() - relativedelta(months=3):
        if current_date.weekday() in range(5):  # 0=Monday, 4=Friday
            weekdays.append(current_date)
        current_date -= datetime.timedelta(days=1)

    weekdays = weekdays[::-1]
    for wd in weekdays:
        # get wallet positions at the given date
        hist_wallets = Wallet.objects.filter(user=user, date__lte=wd).filter(Q(active=True) | Q(closed_at__gt=wd))
        p, cp = 0, 0
        skip = False
        for hw in hist_wallets:
            p += hw.qtd * float(hw.price)
            old_price = get_historical_data(hw.ticker, wd)
            if old_price is None:
                skip = True
                break
            cp += hw.qtd * float(old_price)
        if skip:
            continue
        historical_x.append(wd.strftime('%Y-%m-%d'))
        historical_position.append(round(p,2))
        historical_current_position.append(round(cp,2))
    
    
    return render(request, "app/index.html", {'entries': entries, 
    'position': position, 
    'current_position': current_position, 
    'revenue': revenue, 
    'historical_position': json.dumps(historical_position), 
    'historical_current_position': json.dumps(historical_current_position), 
    'historical_x': json.dumps(historical_x)})

@login_required
def add_entry(request):
    ticker = request.POST.get('ticker', '').upper()
    date = datetime.datetime.strptime(request.POST.get('date', ''), '%Y-%m-%d')
    price = float(request.POST.get('price', '').replace(',', '.'))
    qtd = request.POST.get('qtd', '')

    if is_ticker_valid(ticker) is False:
        messages.error(request, "Ticker inválido!")
        return redirect('index')

    Wallet.objects.create(ticker=ticker, date=date, qtd=qtd, price=price, user=request.user)
    messages.success(request, "Adicionado com sucesso!")
    return redirect('index')

@login_required
def remove_entry(request, id):
    wallet = Wallet.objects.get(id=id)
    # Check if user is the owner of the entry
    if wallet.user != request.user:
        messages.error(request, "Você não tem permissão para remover esta entrada!")
        return redirect('index')
    wallet.active = False
    wallet.closed_at = datetime.datetime.now()
    wallet.save()
    return redirect('index')

@login_required
def delete_entry(request, id):
    wallet = Wallet.objects.get(id=id)
    # Check if user is the owner of the entry
    if wallet.user != request.user:
        messages.error(request, "Você não tem permissão para remover esta entrada!")
        return redirect('index')
    wallet.delete()
    return redirect('index')

@login_required
def history(request):
    wallets = Wallet.objects.filter(user=request.user).order_by('-date')
    return render(request, "app/list.html", {'entries': wallets})