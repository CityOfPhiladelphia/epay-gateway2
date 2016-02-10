from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.conf import settings
from epay import models
import stripe


def epay_js_view(request):
    return render(request, 'epay/epay.js')


def charge_view(request, product_slug):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    stripe_token = request.POST['token[id]']
    stripe_email = request.POST['token[email]']
    stripe.api_key = settings.STRIPE_SECRET_KEY

    product = get_object_or_404(models.Product, slug=product_slug)

    try:
        charge = stripe.Charge.create(
            amount=int(product.price * 100),
            currency='usd',
            card=stripe_token,
            description=str(invoice),
            metadata={
                'name': invoice.recipient.name,
                'organization': invoice.recipient.organization,
                'email': invoice.recipient.email,
                'phone': invoice.recipient.phone,
                'receipt_email': stripe_email,
                'statement_descriptor': request.POST.get('statement_descriptor', None)
            }
        )
        messages.success(request, 'Thank you for your payment on <i>{}</i>!'.format(invoice))

    except stripe.error.StripeError as e:
        messages.error(request, ('There was an error processing your payment: {}. '
            'Please try again, or contact us if you\'re having trouble.').format(e))

    else:
        invoice.payments.add(InvoicePayment(
            amount=charge.amount / 100,
            paid_at=now(),
            stripe_charge_id=charge.id
        ))

    return HttpResponseRedirect(reverse('view-invoice', kwargs={'pk': '{:0>5}'.format(invoice_pk)}) + '?key=' + access_code)
