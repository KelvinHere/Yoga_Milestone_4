# Testing Documentation for Social Yoga

### Manual Tests

- Users can:
    - View a list of instructors
    - View an instructors profile

- Users cannot:
    - View profiles of non-instructors

- Instructor can:
    - Create a lesson
    - Delete a lesson
    - Create a lesson with the same name as another instructor (ie, 'Introduction Lesson')
    - Edit their own lessons

- Instructor cannot:
    - Create two lessons with the same name
    - Edit another instructors lessons

#### Home Page

- **Valid requests**
- While logged in, superusers can access "Superuser admin" where they can
    - Accept/reject users requests to become an instructor
    - Remove instructor status from an instructor

- **Error and Invalid request handling**
- While logged out, users cannot access the following views
    - `/superuser_admin` - Result "Error message - Sorry only administrators can do this"
    - `/update_instructor_status/<user_to_update>/<status>` - Result "Error message - Sorry only administrators can do this"

- While logged in, non superusers cannot access the following views
    - `/superuser_admin` - Result: Redirect to login page
    - `/update_instructor_status/<user_to_update>/<status>` - Result: Redirect to login page

#### Lessons Page

1. **lessons view**
- **Valid requests**
- Filters
    - When directed to the lesson page from the instructors page you are shown the instructor profile with their (sortable and filterable) lessons underneath.
    - Subscribed Lessons filter `/lessons/?filter=mylessons` only displays lessons currently subscribed to, a message of "You are currently not subscribed to any lessons"
    - Purchased Lessons filter `/lessons/?filter=paidlessons` only displays purchased lessons, when a user has none it show the warning "You have not purchased any lessons"
    - All Lessons filter `/lessons/?filter=None` displays all lessons

- Stacked Filters
    - When viewing an instructors lessons
        - All lessons filter will only show lessons by that instructor as default
        - Purchased lessons filter will only show lessons purchased from that instructor
        - Subscribed lessons filter will only show lessons subscribed to from that instructor


- **Error and Invalid request handling**
- Filters
    - `/lessons/?filter=AN_INVALID_FILTER` - Invalid filters default to showing all lessons and will not return an error message

- Sort direction
    - `lessons/?direction=INVALID_DIRECTION` - Invalid direction argument will default the sort to descending
    - `lessons/?sort=INVALID_SORT_ARGUMENT` - Invalid sort arguments will warn the user "Invalid sort value, displaying all lessons by name in ascending order"

- Instructor
    - `lessons/?instructor=NOT_AN_INSTRUCTOR` Passed a user that is not an instructor, user redirected to instructors page error message "This user is not an instructor, please pick one from the instructor list."
    - `lessons/?instructor=INVALID_USER` Passed a user that does not exist, user redirected to instructor page with error message "This instructor was not found, please pick one from the instructor list."

2. **subscribe view**
- **Valid Requests**
    - When passed a valid lesson_id along with
        - `subscribe=true` the user is subscribed to the lesson and JS updates the buttons from "Subscribe" to "Unsubscribe" and "Sart Lesson"
        - `subscribe=false` the user is unsubscribed to the lessons and JS updates the buttons from "Unsubscribed" and "Start Lesson" to "Subscribe"

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - Trying to submit an invalid lesson_id `/lessons/subscriptions/?subscribe=true&lesson_id=INVALID_LESSON_ID` returns user to lessons page with the error message "Invalid request, no lessons have been subscribed or unsubscribed to."
    - Trying alter subscription status of a lesson using something other than `true` or `false` returns the user to lessons page and gives the error message "Invalid request, no lessons have been subscribed or unsubscribed to."
    - A nonsense request with invalid GET keys passed returns user to the lesson page with an error message "Invalid request, no lessons have been subscribed or unsubscribed to."

3. **instructor_created_lessons view**
- **Valid requests**
    - Displays a list of lessons the logged in instructor has created or a prompt "You have not created any lessons yet"

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - If user is not an instructor they are returned to the homepage with the error message "Only instructors can do this"

4. **delete_instructor_created_lesson view**
- **Valid requests**
    - If an instructor passes a valid lesson_id and the logged in profile matches the profile of the lesson creator, the lesson is delete_instructor_created_lesson

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to pass the lesson_id from a lesson they did not create they are given the error message "This lesson does not belong to you and has not been deleted, please check your username and try again."
    - If an instructor tries to pass an invalid lesson_id they are given the error message "Invalid lesson ID, no lessons were deleted."

5. **create_lesson view**
- **Valid requests**
    - GET request will display a lesson creation form to the user
    - POST request will create a lesson from the form data and return the user to their created lesson list

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to create a lesson with the same name as one of their existing lessons they are directed back to their created lessons page with the error message "You already have a lesson named this."
        - Regarding duplicate names, different instructors can have lessons with the same name to avoid "reserving" of popular names such as simple yoga poses, ie both 'Benny' and 'Charle' can have a lesson named 'Mountain Pose'


6. **edit_lesson view**
- **Valid requests**
    - GET requests given a valid lesson_id will display a pre-filled lesson form ready for editing
    - POST requests will update a lesson with the new form data

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to POST data to an invalid lesson_id they are redirected to their created lessons page with the error message "Invalid lesson ID, no lessons were updated."
    - if an instructor tried to GET another instructors lesson_id they are redirected to their created lessons page with the error message "You can only edit your own lessons, please check your username."

7. **review_lesson**
- **Valid requests**
    - GET request will display a review form for the lesson or pre-fill the form with the existing review for editing
    - POST request will create a new review or update an existing review if available

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - User who passes an invalid lesson_id will be redirected home with the error "Cannot create/edit a review for an invalid lesson."
    - User who submits an invalid form are redirected back to the current lesson they were creating a review for with the error message "Error in review form: {form.errors}"


 ## Bugs

- **'Sort lesson by rating - high to low' feature had all non-rated lessons listed at the top**
- Situation - Code would show unrated lessons higher than rated lessons, original code below
    - `lessons = lessons.order_by(sortkey)`

- Task - Get unrated lessons to appear at the bottom of the sorted list

- Action - I used djangos F() expresson and nulls_last argument to sort null/None items to the bottom of the list, new code below
    - `if sort_direction == 'asc':`
        - `lessons = lessons.order_by(F(sortkey).asc(nulls_last=True))`
    - `else:`
        - `lessons = lessons.order_by(F(sortkey).desc(nulls_last=True))`

- Result - The lessons are now sorted correctly, though I cant append a simple tag `-` to reverse the sort direction so an if else statement is used instead

- **User not logged in**
- Situation - A lot of features on this site require a user profile to function properly, catering to anonymous users involved a lot of code to `try:` getting the userprofile with `get_object_or_404` bloating code

- Task - Reduce this pattern in the code by following the DRY principle

- Action - I created a utility in the main app directory `yoga.utils.py` that contains a function that recieves a request and tries to get a profile from it or returns none.

- Result - Any part of the app where it matters if a user is logged in or not will use a single line `get_profile_or_none(request)` to return a valid profile or a None object, reducing patterns in the code.

