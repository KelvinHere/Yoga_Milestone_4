// Replace button href with new lesson href
function delete_lesson_modal(lesson_id) {
    $('#modal-delete-button').attr('href', lesson_id)
    $('#delete-lesson-modal').modal('show');
}