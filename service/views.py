import os
import stripe
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from service.forms import *
from service.models import Item
from PaymentService.settings import MEDIA_ROOT, STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

log = logging.getLogger(__name__)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def item_by_id(request, item_id):
    context = __get_basic_context()

    context["item"] = Item.objects.get(id=item_id)

    return render(request, "item_page.html", context)


@csrf_exempt
def buy_by_id(request, item_id):
    context = __get_basic_context()

    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = STRIPE_SECRET_KEY

        item = Item.objects.get(id=item_id)
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
                        'unit_amount': int(item.price.amount*100),
                        'product_data': {
                            'name': item.title,
                            'description': item.description,
                            # 'images': ['https://example.com/t-shirt.png'],
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

    return render(request, "buy_page.html", context)


def __get_basic_context():
    context = dict()

    context["images_root"] = os.sep + os.path.basename(os.path.normpath(MEDIA_ROOT)) + os.sep

    return context
