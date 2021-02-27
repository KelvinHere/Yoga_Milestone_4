//  Hides the lesson form and displays a spinner when form is submitted
$( document ).ready(function() {
    let form = document.getElementById('lesson-form');
    form.addEventListener('submit', function(event) {
        $('#lesson-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);
    });
});
