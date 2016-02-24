from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed
from django.conf import settings
from epay import models
import json
import stripe


def epay_js_view(request):
    return render(request, 'epay/epay.js')

def get_product_data(key):
    ## TODO: Think about how to retrieve product information when
    #        we can use the local database or a remote API, etc.
    return get_object_or_404(models.Product, slug=key)


# API Views
# ~~~~~~~~~

"""
/invoice

    POST
    ----
    Create a new invoice.

/pay

    POST
    ----
    Pay an existing invoice

/invoice-and-pay

    POST
    ----
    Create a new invoice and pay it.

/invoice/:id

    GET
    ---
    Retrieve the status and amount paid on an invoice.

"""


@csrf_exempt
def charge_view(request, product_slug=None):
    if request.method not in ['POST']:
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    stripe_token = request.POST['token[id]']
    stripe_email = request.POST['token[email]']
    stripe.api_key = settings.STRIPE_SECRET_TOKEN

    product = get_product_data(product_slug)

    try:
        charge = stripe.Charge.create(
            amount=int(product.price * 100),
            currency='usd',
            card=stripe_token,
            description=str(product.name),
            #metadata={
            #    'name': invoice.recipient.name,
            #    'organization': invoice.recipient.organization,
            #    'email': invoice.recipient.email,
            #    'phone': invoice.recipient.phone,
            #    'receipt_email': stripe_email,
            #    'statement_descriptor': request.POST.get('statement_descriptor', None)
            #}
        )

    except stripe.error.StripeError as e:
        response_data = {
            'status': 'error',
            'message': ('There was an error processing your payment: {}. '
                        'Please try again, or contact us if you\'re having '
                        'trouble.').format(e)
        }

    else:
        response_data = {
            'amount': charge.amount / 100,
            'last4': charge.source.last4,
            'status': 'success',
        }

        ## TODO: Should we log transactions?

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')
