// Replace button href with new lesson href
//  jshint esversion: 6

function delete_lesson_modal(lesson_id) {
    $('#modal-delete-button').attr('href', lesson_id);
    $('#delete-lesson-modal').modal('show');
}