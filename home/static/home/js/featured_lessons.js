// Script for showing hiding and cycling featured lessons

// Display random lessons with delay
$(document).ready(function() {
    // Get Lessons and convert to json object
    let lessons = document.getElementById("json_lessons").textContent.trim()
    let json_lessons = JSON.parse(lessons)
    let size = Object.keys(json_lessons).length
    let count = 1
    let mediaUrl = $('#media_url_id').text().slice(1,-1);
    let studioUrl = $('#studio_url_id').text().trim().slice(1,-1);

    // Setup first featured lesson
    $('#featured-title').text(json_lessons[count % size].lesson_name);
    $('#featured-image').attr("src",mediaUrl + json_lessons[count % size].image);
    $('#featured-image-link').attr('href', studioUrl.replace('lesson_id', json_lessons[count % size].lesson_id));
    count++;
    
    setInterval (function() {
        // Change title
        $('#featured-title').text(json_lessons[count % size].lesson_name);
        $('#featured-image').fadeTo(50, 0.01, function(){
            // Swap image
            $('#featured-image').attr("src",mediaUrl + json_lessons[count % size].image);
            // Change link
            $('#featured-image-link').attr('href', studioUrl.replace('lesson_id', json_lessons[count % size].lesson_id));
            count++;
            $(this).delay(50).fadeTo(50, 1);
        });
    }, 7000);
});

// Toggle featured lessons
function toggle_featured(){
    $('#featured-lessons').toggle();
};
