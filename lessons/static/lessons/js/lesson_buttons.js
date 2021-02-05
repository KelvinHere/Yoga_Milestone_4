// Handle subscribe / unsubscribe / start_lesson buttons
function subscribe(subscribe, lesson_id, filter) {
    $.ajax({
        type:"GET",
        url:"/lessons/subscriptions",
        data:{  
            subscribe: subscribe,
            lesson_id: lesson_id,
        },
        success: function(json_response){
            if (json_response['subscription_status'] == 'unsubscribed') {
                // Unsub button
                $('#unsubscribe_lesson_button_id_'+lesson_id).hide();
                // Sub button
                $('#subscribe_lesson_button_id_'+lesson_id).removeAttr('hidden');
                $('#subscribe_lesson_button_id_'+lesson_id).show();
                // Start Lesson button
                $('#start_lesson_button_id_'+lesson_id).hide();
                if (filter == 'mylessons') {
                    $('#'+lesson_id).remove();
                }
            } else if (json_response['subscription_status'] == 'subscribed') {
                // Unsub button
                $('#unsubscribe_lesson_button_id_'+lesson_id).removeAttr('hidden');
                $('#unsubscribe_lesson_button_id_'+lesson_id).show();
                // Sub button
                $('#subscribe_lesson_button_id_'+lesson_id).hide();
                // Start Lesson button
                $('#start_lesson_button_id_'+lesson_id).removeAttr('hidden');
                $('#start_lesson_button_id_'+lesson_id).show();
            }
        }
    })
}

// Create added to basket popover
$('#navbar-basket').popover({
    content: "Your lesson has been added to the basket",
    html: true,
    placement: 'bottom',
    trigger: 'manual'
});

// Handle add to basket requests via AJAX
function add_to_basket(lesson_id) {
    let csrfToken = "{{ csrf_token }}";
    event.preventDefault();
    $.ajax({
        type:"POST",
        url:"/basket/add_to_basket/",
        data:{  
            'csrfmiddlewaretoken': csrfToken,
            lesson_id: lesson_id,
        },
        success: function(json_response){
            if (json_response['item_added'] == 'True'){
                // Increment item count on navbar basket button
                let count = String($('#nav-cart-amount').text());
                count = count.replace('+', '');
                count = parseInt(count);
                if (Number.isNaN(count)) {
                    count = 1;
                } else {
                    count = count + 1;
                }
                $('#nav-cart-amount').text('+'+count);
                $('#add_'+lesson_id).text('Added')
                // Popover to confirm item has been added
                $('#navbar-basket').popover('toggle');
                // Change banner to show discount is applied if discount delta = 0
                if (json_response['discount_delta'] == true) {
                    $('#discount-applied').removeAttr('hidden')
                    $('#discount-not-applied').hide()
                }
            } else if (json_response['item_added'] == 'already_added'){
                // Create already_added to button popover
                $('#add_'+lesson_id).popover({
                    content: "You have already added this to your basket",
                    html: true,
                    placement: 'bottom',
                    trigger: 'manual'
                });
                $('#add_'+lesson_id).popover('toggle');
            } else {
                // Item does not exist to button popover
                $('#add_'+lesson_id).popover({
                    content: "There is a problem with this lesson, please refresh your browser and try again",
                    html: true,
                    placement: 'bottom',
                    trigger: 'manual'
                });
                $('#add_'+lesson_id).popover('toggle');
            }
        }
    })
}

// Handle modal requests via AJAX
function get_modal_data(lesson_id) {
    let csrfToken = "{{ csrf_token }}";
    event.preventDefault();
    $.ajax({
        type:"POST",
        url:"/lessons/get_modal_data/",
        data:{  
            'csrfmiddlewaretoken': csrfToken,
            lesson_id: lesson_id,
        },
        success: function(json_response){
            if (json_response['status'] = 'valid_lesson'){
                $('#modal-container').empty();
                $('#modal-container').html(json_response['modal']);
                $('#moreDetailsModal').modal('show');
            }
        }
    })
}
