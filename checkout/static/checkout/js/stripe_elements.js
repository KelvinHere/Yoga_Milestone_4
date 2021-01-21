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
var card = elements.create('card', {style: style});
card.mount('#card-element');

//Handle realitime card validation errors, display under card element
card.addEventListener('change', function(event) {
    var errorMessageDiv = document.getElementById('card-error-messages');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-exclamation-circle"></i>
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
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            var errorMessageDiv = document.getElementById('card-error-messages');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-exclamation-circle"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            $(errorMessageDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});