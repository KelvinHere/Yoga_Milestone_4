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
- While logged out, users cannot access the following views
    - `/superuser_admin` - Result "Error message - Sorry only administrators can do this"
    - `/update_instructor_status/<user_to_update>/<status>` - Result "Error message - Sorry only administrators can do this"


- While logged in, non superusers cannot access the following views
    - `/superuser_admin` - Result: Redirect to login page
    - `/update_instructor_status/<user_to_update>/<status>` - Result: Redirect to login page

#### Lessons Page
- Filters
    - `/lessons/?filter=AN_INVALID_FILTER` - Invalid filters default to showing all lessons and will not return an error message
    - `/lessons/?filter=paidlessons` - paidlesson filter when user has none will show the warning "You have not purchased any lessons"
    - `/lessons/?filter=mylessons` - mylessons (subscribed lessons) when user has none will show the warning "You are currently not subscribed to any lessons"

- Sort direction
    - `lessons/?direction=INVALID_DIRECTION` - Invalid direction argument will default the sort to descending
    - `lessons/?sort=INVALID_SORT_ARGUMENT` - Invalid sort arguments will warn the user "Invalid sort value, displaying all lessons by name in ascending order"

- Instructor
    - When directed to the lesson page from the instructors page you are shown the instructor profile with their (sort and filterable )lessons underneath
    - `lessons/?instructor=NOT_AN_INSTRUCTOR` Passed a user that is not an instructor, user redirected to instructors page with error "This user is not an instructor, please pick one from the instructor list."
    - `lessons/?instructor=INVALID_USER` Passed a user that does not exist, user redirected to instructor page with error "This instructor was not found, please pick one from the instructor list."

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

