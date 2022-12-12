//  Create and style card element
//  jshint esversion: 6
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#534a47',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#534a47'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {hidePostalCode: true, style: style});
card.mount('#card-element');

//  Handle realitime card validation errors, display under card element
card.addEventListener('change', function(event) {
    var errorMessageDiv = document.getElementById('card-error-messages');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-exclamation-circle text-warning"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorMessageDiv).html(html);
    } else {
        errorMessageDiv.textContent = '';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    
    // Prepare data to be posted to attach_basket_to_intent view
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret
    };
    var url = '/checkout/attach_basket_to_intent/';

    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    email: $.trim(form.email.value),
                }
            }
        }).then(function(result) {
            if (result.error) {
                var errorMessageDiv = document.getElementById('card-error-messages');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-exclamation-circle text-warning"></i>
                    </span>
                    <span>${result.error.message}</span>
                `;
                $(errorMessageDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // Reload the page to show the passed error message from attach_basket_to_intent
        location.reload();
    });
});
