var epay = epay || {};

(function() {

    "use strict";

    epay.initPaymentForm = function(options) {
        var product = options.product;
        var success = options.succes;
        var error = options.error;
        var data = options.data;

        // document.write(
        //   '<script src="https://code.jquery.com/jquery-2.2.0.min.js"></script>' +
        //   '<script src="https://checkout.stripe.com/checkout.js"></script>' +
        //   '<button id="customButton">Click Here</button>'
        // );

        var handler = StripeCheckout.configure({
            key: "pk_test_6pRNASCoBOKtIshFeQd4XMUh",
            image: "/square-image.png",
            token: function(token, args) {
                $.ajax({
                    url: "http://localhost:50856/charge/" + product + "/",
                    type: "POST",
                    dataType: 'json',
                    //contentType: "application/json; charset=utf-8",
                    data: _.extend(data, { token: token }),
                    success: success,
                    error: error
                });
            }
        });

        document.getElementById("customButton").addEventListener("click", function(e) {
            handler.open({
                name: "Demo Site",
                description: "3 widgets ($50.00)",
                amount: 5000
            });
            e.preventDefault();
        });

        // document.write(
        //   '<form action="" method="POST" id="paymentform">' +
        //   '  <script' +
        //   '    src="https://checkout.stripe.com/checkout.js" class="stripe-button"' +
        //   '    data-key="pk_test_6pRNASCoBOKtIshFeQd4XMUh"' +
        //   '    data-image="/img/documentation/checkout/marketplace.png"' +
        //   '    data-name="Stripe.com"' +
        //   '    data-description="2 widgets"' +
        //   '    data-amount="2000"' +
        //   '    data-locale="auto">' +
        //   '  </script>' +
        //   '</form>'
        // );
    };
})();