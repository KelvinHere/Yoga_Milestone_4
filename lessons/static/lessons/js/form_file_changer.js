// Controls content for changing an image file
//  jshint esversion: 6

$(document).ready(function() {      
    // Remove unwanted content
    let el = $('#change-image');
    let label = $('#id_image_label');
    let input_button = $('#id_image');

    el.empty().append(label).append(input_button);

    // Style
    let input_new = $('#id_image');
    el.addClass("mb-4");
    input_new.addClass("btn btn-custom-darken");

    // Update name on file change
    $('#id_image').change(function(){
        let fileName = event.target.value;
        
        // windows vs linux directory seperator
        fileName = fileName.replace('/', '\\');
        
        // split by \
        let split = fileName.split("\\");
        $('#current-image-container').empty();
        $('#current-image-container').html("<p>Update image to <strong>" + split.slice(-1) + "</strong></p>");
    });
});