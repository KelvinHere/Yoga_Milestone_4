// Handle subscribe / unsubscribe / start_lesson buttons
function delete_lesson_modal(lesson_id) {
    $('#modal-footer').prepend( `
        <a class="btn btn-danger instructor-admin-button" href="{% url 'delete_lesson' ` + lesson_id + ` %}" role="button">
            Yes, Delete
        </a>` );
    $('#delete-lesson-modal').modal('show');
}