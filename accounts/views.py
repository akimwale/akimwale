from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import auth, Group, User
from django.contrib import messages
from telusko_app.decorators import unauthorized, allowed_users, admin_only
from telusko_app.views import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import *
from .forms import *
from .filter import order_search
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache
import datetime
from django.utils import timezone
import json
import re
import os
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from django.forms import modelform_factory
from .models import CryptoTransaction
import hashlib
import hmac
import requests
import time
import stripe

logger = logging.getLogger(__name__)

@user_passes_test(unauthorized, login_url='/')

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     user = user,
            # )
            messages.success(request, 'Account was created for ' +  username)
            # Create a notification for successful booking
            

            return redirect('/login')

    context = {'form':form}
    return render(request, 'signup.html', context)


def unauthorized(user):
    return not user.is_authenticated


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            Notification.objects.create(
                user=user,
                message=f"You have been successfully logged in at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}."
            )
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')

@csrf_exempt
def predefined_messages(request):
    if request.method == 'GET':
        messages = FAQ.objects.values_list('question', flat=True)
        return JsonResponse({'messages': list(messages)})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            faq = FAQ.objects.filter(question__icontains=question).first()
            response = {'answer': faq.answer if faq else 'Sorry, I don\'t have an answer for that question, but you can talk directly to customer supprt on the home page.'}
            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def chatter(request):
    user_profile = Customer.objects.get(user=request.user)
    faqs = FAQ.objects.all()
    return render(request, 'chatbot.html', {'faqs': faqs, 'user_profile':user_profile})

@login_required(login_url='login')
def profile(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    market_data, trending_data = fetch_crypto_data()
    portfolio = Portfolio.objects.get(user=request.user)
    orders = customer.order_set.all()
    product = Product.objects.all()
    total_orders = orders.count()
    pending = orders.filter(status='Pending').count()
    completed = orders.filter(status='Completed').count()
    satisfied = orders.filter(status='Satisfied').count()
    unread_notifications_count = request.user.notifications.filter(read=False).count()
    
    search_term = request.GET.get('search', '')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        
            # Create a notification for profile update
            Notification.objects.create(
                user=request.user,
                message="Your profile has been updated successfully."
            )
            
            return redirect('profile', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    
    if market_data and trending_data:
        # Extract relevant information
        market_cap = market_data['data']['total_market_cap']['usd']
        trading_volume = market_data['data']['total_volume']['usd']
        trending_coins = trending_data['coins']
    context = {
        'customer': customer, 
        'orders': orders, 
        'total': total_orders, 
        'pending': pending, 
        'completed': completed, 
        'satisfied': satisfied, 
        'form': form,
        'search_term': search_term,
        'unread_notifications_count': unread_notifications_count,
        'product':product,
        'portfolio':portfolio,
        'trending_coins': trending_coins,
        }
    
    return render(request, 'profiled.html', context)

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': user_notifications})

from django.http import HttpResponseRedirect
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return HttpResponseRedirect('/notifications/')

@login_required
def mark_as_unread(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = False
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return JsonResponse({'status': 'success'})


def purchase_recovery_key(request):
    customer = Customer.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = RecoveryKeyRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/digital')  # Redirect to a success page or handle accordingly
        # If form is not valid, it will retain the submitted data and display errors
    else:
        form = RecoveryKeyRequestForm()  # Initialize an empty form on GET request

    return render(request, 'recovery.html', {'form': form, 'customer': customer})


def keys(request):
    keys = DigitalKey.objects.all()
    
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'keys.html', {'keys': keys, 'customer': customer})
        else:
            return render(request, 'keys.html', {'keys': keys, 'error': 'No customer profile found.'})
    
    return render(request, 'keys.html', {'keys': keys})

from django.shortcuts import get_object_or_404, render, redirect
from .models import DigitalKey, Customer
from .forms import PaymentForm

def payment_page(request, pk):
    digital_key = get_object_or_404(DigitalKey, pk=pk)

    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            return render(request, 'payment_page.html', {'error': 'No customer profile found.'})

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Handle payment processing
            return redirect('payment_success')
    else:
        form = PaymentForm(initial={'key': digital_key})
        messages.error(request, 'There was an error with your submission. Please check the form and try again.')

    context = {
        'form': form,
        'key': digital_key,
        'customer': customer if request.user.is_authenticated else None,
    }

    return render(request, 'payment_page.html', context)




from django.shortcuts import redirect

def gift_card_payment(request, pk):
    digital_key = get_object_or_404(DigitalKey, pk=pk)


    if request.method == 'POST':
       form = GiftCardPaymentForm(request.POST, request.FILES)
       print(messages.error)
       if form.is_valid():
           form.save()
           messages.success(request, 'Payment processed successfully!')
           return redirect('payment_success')
       else:
            for field, errors in form.errors.items():
              for error in errors:
                 messages.error(request, f'{field}: {error}')
                 
            messages.info(request, f'There was an error with your submission. Please check the form and try again.')        
    else:
        form = GiftCardPaymentForm()
        
    
    return render(request, 'gift_card_page.html', {'form': form, 'digital_key': digital_key})

def crypto_payment(request, pk):
    digital_key = get_object_or_404(DigitalKey, pk=pk)

    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            # Get the crypto wallet details, including network cost
            bitcoin_wallet = CryptoWallet.objects.filter(currency='bitcoin').first()
            usdt_wallet = CryptoWallet.objects.filter(currency='usdt').first()
            ethereum_wallet = CryptoWallet.objects.filter(currency='ethereum').first()
            
            # Prepare the context for rendering
            context = {
                'customer': customer,
                'bitcoin_address': bitcoin_wallet.address if bitcoin_wallet else None,
                'bitcoin_network': bitcoin_wallet.get_network_type_display() if bitcoin_wallet else None,
                'bitcoin_cost': bitcoin_wallet.network_cost if bitcoin_wallet else None,
                'usdt_address': usdt_wallet.address if usdt_wallet else None,
                'usdt_network': usdt_wallet.get_network_type_display() if usdt_wallet else None,
                'usdt_cost': usdt_wallet.network_cost if usdt_wallet else None,
                'ethereum_address': ethereum_wallet.address if ethereum_wallet else None,
                'ethereum_network': ethereum_wallet.get_network_type_display() if ethereum_wallet else None,
                'ethereum_cost': ethereum_wallet.network_cost if ethereum_wallet else None,
                'networks': CryptoWallet.objects.all(),
            }
            return render(request, 'crypto_page.html', context)
        else:
            return render(request, 'crypto_page.html', {'error': 'No customer profile found.'})

    # For non-authenticated users or if customer is not found
    return render(request, 'crypto_page.html', {'error': 'User is not authenticated or no customer profile found.', 'key':digital_key})


def transfer_redirect(request, method_name):
    redirect_url = PaymentMethodRedirect.objects.filter(method_name=method_name).first().redirect_url
    return redirect(redirect_url)


def mobile_bank(request):
    profiles = ProfileApp.objects.all()

    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()

        if customer:
            return render(request, 'mobile_bank.html', {'customer': customer, 'profiles': profiles})
        else:
            return render(request, 'mobile_bank.html', {'error': 'No customer profile found.', 'profiles': profiles})

    return render(request, 'mobile_bank.html', {'profiles': profiles})

def get_social_apps(request, profile_id):
    profile = ProfileApp.objects.get(id=profile_id)
    social_apps = profile.social_apps.all()
    social_apps_data = [{
        'name': app.name,
        'image_url': app.image.url,
        'link': app.link
    } for app in social_apps]
    
    return JsonResponse({'social_apps': social_apps_data})


def create_payment(request, digital_key_id):
    digital_key = get_object_or_404(DigitalKey, pk=digital_key_id)
    
    
    if request.method == "POST":
        amount = digital_key.price  # The price of the digital key in USD

        # Prepare CoinPayments API request
        url = 'https://www.coinpayments.net/api.php'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {
            'cmd': 'create_transaction',
            'key': settings.COINPAYMENTS_API_KEY,
            'version': 1,
            'amount': amount,
            'currency1': 'USD',
            'currency2': 'BTC',  # The cryptocurrency to accept, e.g., BTC, ETH, USDT
            'item_name': digital_key.name,
            'item_number': digital_key_id,
            'invoice': f"{request.user.id}-{digital_key_id}",
            'ipn_url': request.build_absolute_uri('/ipn/'),  # IPN (Instant Payment Notification) URL
            'success_url': request.build_absolute_uri('/payment-success/'),
            'cancel_url': request.build_absolute_uri('/payment-cancelled/'),
        }

        # Generate HMAC signature
        post_data = "&".join([f"{key}={value}" for key, value in payload.items()])
        hmac_signature = hmac.new(
            bytes(settings.COINPAYMENTS_API_SECRET, 'utf-8'),
            bytes(post_data, 'utf-8'),
            hashlib.sha512
        ).hexdigest()
        headers['HMAC'] = hmac_signature

        # Send the request to CoinPayments
        response = requests.post(url, data=payload, headers=headers)

        # Check the response
        try:
            response_data = response.json()  # Attempt to parse JSON response
        except ValueError:
            return render(request, 'payment_error.html', {'error': 'Invalid response from payment gateway.'})
        
        if response.status_code == 200:
            if response_data.get('error') == 'ok':
                transaction_data = response_data.get('result')
                transaction = CryptoTransaction.objects.create(
                    user=request.user,
                    transaction_id=transaction_data['txn_id'],
                    currency='BTC',
                    amount=amount,
                    status='pending'
                )
                return redirect(transaction_data['checkout_url'])
            else:
                # Error returned by the API
                error_message = response_data.get('error')
                return render(request, 'payment_error.html', {'error': error_message})
        else:
            # Non-200 response from the API
            return render(request, 'payment_error.html', {'error': 'Failed to create payment request. Please try again later.'})
    
    # For GET requests, show a confirmation page or form
    return render(request, 'create_payment.html', {'digital_key': digital_key})



def success(request):
    return render(request, 'successful.html')


# crypto/views.py

from django.shortcuts import render
from .services import CoinGeckoService

def crypto_prices(request):
    cg_service = CoinGeckoService()
    prices = cg_service.get_price(ids='bitcoin,ethereum', vs_currencies='usd')
    return render(request, 'crypto_prices.html', {'prices': prices})

def crypto_converter(request):
    cg_service = CoinGeckoService()
    coins = cg_service.get_coins_list()
    return render(request, 'crypto_converter.html', {'coins': coins})




def convert_crypto(request):
    from_currency = request.GET.get('from')
    to_currency = request.GET.get('to')
    amount = request.GET.get('amount', 1)

    if not from_currency or not to_currency:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    try:
        amount = float(amount)
    except ValueError:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    cg_service = CoinGeckoService()
    conversion_rate = cg_service.get_conversion_rate(from_currency, to_currency)

    if conversion_rate and to_currency in conversion_rate:
        converted_amount = amount * conversion_rate[to_currency]
        return JsonResponse({'converted_amount': converted_amount})
    else:
        return JsonResponse({'error': 'Conversion rate not available'}, status=400)


from django.core.cache import cache

# views.py

def fetch_coin_data(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        if response.status_code == 404:
            return {'error': 'Coin not found'}
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

def purchase_page(request):
    symbol = request.GET.get('symbol')
    
    customer = None
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
    if not symbol:
        return HttpResponse('No coin symbol provided', status=400)

    # Map symbols to CoinGecko IDs
    coin_id_map = {
        'btc': 'bitcoin',
'eth': 'ethereum',
'usdt': 'tether',
'bnb': 'binancecoin',
'sol': 'solana',
'usdc': 'usd-coin',
'xrp': 'ripple',
'steth': 'staked-ether',
'ton': 'the-open-network',
'doge': 'dogecoin',
'ada': 'cardano',
'trx': 'tron',
'wsteth': 'wrapped-steth',
'wbtc': 'wrapped-bitcoin',
'avax': 'avalanche-2',
'shib': 'shiba-inu',
'weth': 'weth',
'bch': 'bitcoin-cash',
'dot': 'polkadot',
'link': 'chainlink',
'leo': 'leo-token',
'dai': 'dai',
'ltc': 'litecoin',
'uni': 'uniswap',
'near': 'near',
'weeth': 'wrapped-eeth',
'kas': 'kaspa',
'matic': 'matic-network',
'icp': 'internet-computer',
'usde': 'ethena-usde',
'pepe': 'pepe',
'apt': 'aptos',
'xmr': 'monero',
'etc': 'ethereum-classic',
'xlm': 'stellar',
'fdusd': 'first-digital-usd',
'cro': 'crypto-com-chain',
'okb': 'okb',
'sui': 'sui',
'stx': 'blockstack',
'fet': 'fetch-ai',
'fil': 'filecoin',
'tao': 'bittensor',
'mnt': 'mantle',
'hbar': 'hedera-hashgraph',
'vet': 'vechain',
'mkr': 'maker',
'arb': 'arbitrum',
'atom': 'cosmos',
'render': 'render-token',
'inj': 'injective-protocol',
'imx': 'immutable-x',
'aave': 'aave',
'op': 'optimism',
'wbt': 'whitebit',
'reth': 'rocket-pool-eth',
'wif': 'dogwifcoin',
'ar': 'arweave',
'grt': 'the-graph',
'meth': 'mantle-staked-ether',
'rune': 'thorchain',
'bgb': 'bitget-token',
'hnt': 'helium',
'bonk': 'bonk',
'not': 'notcoin',
'ezeth': 'renzo-restaked-eth',
'theta': 'theta-token',
'floki': 'floki',
'ftm': 'fantom',
'jup': 'jupiter-exchange-solana',
'tia': 'celestia',
'pyth': 'pyth-network',
'ondo': 'ondo-finance',
'jasmy': 'jasmycoin',
'algo': 'algorand',
'gt': 'gatechain-token',
'ldo': 'lido-dao',
'kcs': 'kucoin-shares',
'core': 'coredaoorg',
'qnt': 'quant-network',
'sei': 'sei-network',
'eeth': 'ether-fi-staked-eth',
'bsv': 'bitcoin-cash-sv',
'pyusd': 'paypal-usd',
'ftn': 'fasttoken',
'flow': 'flow',
'brett': 'based-brett',
'usdd': 'usdd',
'eos': 'eos',
'msol': 'msol',
'om': 'mantra-dao',
'egld': 'elrond-erd-2',
'btt': 'bittorrent',
'flr': 'flare-networks',
'dydx': 'dydx-chain',
'axs': 'axie-infinity',
'rseth': 'kelp-dao-restaked-eth',
'neo': 'neo',
'gala': 'gala',
'tkx': 'tokenize-xchange',
    }

    coin_id = coin_id_map.get(symbol.lower())
    if not coin_id:
        return HttpResponse('Invalid coin symbol', status=400)

    coin_data = fetch_coin_data(coin_id)
    if 'error' in coin_data:
        return HttpResponse(f'Error fetching coin data: {coin_data["error"]}', status=500)

    return render(request, 'purchase.html', {'coin': coin_data, 'customer':customer})


from django.views.decorators.http import require_POST
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@require_POST
@csrf_exempt
def process_payment(request):
    symbol = request.POST.get('symbol')
    quantity = request.POST.get('quantity')

    

    if not symbol or not quantity:
        return HttpResponse('Symbol or quantity not provided', status=400)
    
    try:
        quantity = int(quantity)
    except ValueError:
        return HttpResponse('Invalid quantity provided', status=400)

    # Map symbols to CoinGecko IDs
    coin_id_map = {
        'bitcoin': 'bitcoin',
        'btc': 'bitcoin',
        'ethereum': 'ethereum',
        'eth': 'ethereum',
        'ripple': 'ripple',
        'xrp': 'ripple',
    }

    coin_id = coin_id_map.get(symbol.lower())
    if not coin_id:
        return HttpResponse('Invalid coin symbol', status=400)

    # Fetch coin data to get the price
    coin_data = fetch_coin_data(coin_id)
    if 'error' in coin_data:
        return HttpResponse(f'Error fetching coin data: {coin_data["error"]}', status=500)
    
    price = coin_data['market_data']['current_price']['usd']
    amount = int(price * quantity * 100)  # Convert to cents

    # Create a Stripe Checkout session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{symbol.upper()} Purchase',
                    },
                    'unit_amount': amount,
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as e:
        return HttpResponse(f'Payment failed: {e.user_message}', status=500)
    

def checkout(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))  # Amount in cents
        email = request.POST.get('email')
        token = request.POST.get('stripeToken')

        try:
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                customer=customer.id,
                description='Example charge'
            )
            return redirect('success')
        except stripe.error.CardError as e:
            return HttpResponse(f'Payment failed: {e.user_message}', status=500)

    # Render checkout page with Stripe public key
    return render(request, 'checkout.html', {'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY})

def cancel(request):
    return render(request, 'cancel.html')



def fetch_crypto_data():
    market_data_response = requests.get('https://api.coingecko.com/api/v3/global')
    trending_response = requests.get('https://api.coingecko.com/api/v3/search/trending')

    if market_data_response.status_code == 200 and trending_response.status_code == 200:
        market_data = market_data_response.json()
        trending_data = trending_response.json()
        return market_data, trending_data
    else:
        return None, None

def crypto_dashboard(request):
    market_data, trending_data = fetch_crypto_data()
    customer = None
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()

    if market_data and trending_data:
        # Extract relevant information
        market_cap = market_data['data']['total_market_cap']['usd']
        trading_volume = market_data['data']['total_volume']['usd']
        trending_coins = trending_data['coins']

        # Fetch largest gainers (top 10 by market cap)
        gainers_response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params={
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': False,
        })

        if gainers_response.status_code == 200:
            gainers_coins = gainers_response.json()
        else:
            gainers_coins = []

        # Pass data to the template
        context = {
            'customer': customer,
            'market_cap': market_cap,
            'trading_volume': trading_volume,
            'trending_coins': trending_coins,
            'gainers_coins': gainers_coins,
        }

        return render(request, 'crypto_prices.html', context)
    else:
        # Handle API errors
        return render(request, 'crypto_prices.html', {
            'customer': customer,
            'error': 'Failed to retrieve cryptocurrency data. Please try again later.'
        })


from django.utils import timezone
from decimal import Decimal
import datetime

def update_profit(portfolio):
    time_elapsed = timezone.now() - portfolio.last_profit_update
    hours_elapsed = time_elapsed.total_seconds() / 3600
    profit_increment = (Decimal(0.3) / 100) * portfolio.balance * Decimal(hours_elapsed)
    portfolio.profit += profit_increment
    portfolio.last_profit_update = timezone.now()
    portfolio.save()

def portfolio_view(request):
    portfolio = Portfolio.objects.get(user=request.user)

    if request.method == 'POST':
        form = HoldingForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            amount = form.cleaned_data['amount']

            # Check if the holding already exists
            holding, created = Holding.objects.get_or_create(portfolio=portfolio, symbol=symbol)

            try:
                if created:
                    holding.amount += amount
                else:
                    holding.amount = amount  # Add to existing amount

                holding.save()
                messages.success(request, f'Holding for {symbol} updated successfully.')
            except IntegrityError:
                messages.error(request, 'There was an issue updating your holding. Please try again.')

            return redirect('/portfolio')
        else:
            messages.error(request, 'Invalid input. Please check your form.')
    else:
        form = HoldingForm()

    holdings = portfolio.holdings.all()

    context = {
        'portfolio': portfolio,
        'holdings': holdings,
        'form': form,
    }
    return render(request, 'portfolio.html', context)


def deposit(request):
    if request.method == 'POST' and request.user.is_authenticated:
        amount = Decimal(request.POST.get('amount'))
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += amount
        wallet.save()

        # Record the transaction
        Transaction.objects.create(wallet=wallet, amount=amount, transaction_type='deposit')

        # Update portfolio balance
        portfolio = Portfolio.objects.get(user=request.user)
        portfolio.balance += amount
        portfolio.save()

        return redirect('portfolio_view')
    return render(request, 'deposit.html')

@login_required
def deposit_view(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            portfolio.balance += amount
            portfolio.save()
            messages.success(request, f'Successfully deposited ${amount:.2f} to your portfolio!')
            return redirect('portfolio_view')
    else:
        form = TransactionForm()
    return render(request, 'deposit.html', {'form': form, 'portfolio': portfolio})

@login_required
def withdrawal_view(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if portfolio.balance >= amount:
                portfolio.balance -= amount
                portfolio.save()
                messages.success(request, f'Successfully withdrew ${amount:.2f} from your portfolio!')
                return redirect('portfolio_view')
            else:
                messages.error(request, 'Insufficient balance! You cannot withdraw more than your current balance.')
        else:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
    else:
        form = TransactionForm()
    return render(request, 'withdrawal.html', {'form': form, 'portfolio': portfolio})




