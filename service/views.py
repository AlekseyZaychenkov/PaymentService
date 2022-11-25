import os
import stripe
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json

from service.forms import *
from service.models import Item
from PaymentService.settings import MEDIA_ROOT, STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

log = logging.getLogger(__name__)


def home(request):
    context = __get_basic_home_context()

    return render(request, "home.html", context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        # 200 == 2,00$
                        'unit_amount': 200,
                        'product_data': {
                            'name': 'T-shirt',
                            'description': 'Comfortable cotton t-shirt',
                            'images': ['https://example.com/t-shirt.png'],
                        },
                    },
                    'quantity': 1,
                }],
                payment_method_types=['card'],
                mode='payment',
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return JsonResponse({'Error': str(e)})


def item_by_id(request, item_id):
    context = __get_basic_home_context()

    context["item"] = Item.objects.get(id=item_id)

    return render(request, "item_page.html", context)


def buy_by_id(request, item_id):
    context = __get_basic_home_context()

    context["item"] = Item.objects.get(id=item_id)

    return render(request, "buy_page.html", context)


def __get_basic_home_context():
    context = dict()

    context["images_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep

    return context
