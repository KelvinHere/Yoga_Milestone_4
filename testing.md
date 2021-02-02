# Testing Documentation for Social Yoga

INDEX  
Index Here  


## Manual Tests
***
## **Site Actions**
- **Users can:**
    - View a list of instructors
    - View lessons by instructor
    - Filter lessons by All / Purchased / Subscribed
    - Sort lessons by price / rating / instructor / name
    - Subscribe / Unsubscribe to a lesson
    - Create / Edit a review for a lesson
    - Access free lessons and lessons they have paid for
    - Add / Remove a lesson from their basket
    - Purchase a lesson
    - Request / Unrequest instructor status

- **Users cannot:**
    - Create / Edit someone elses review of a lesson
    - Access paid lessons they have not purchased

- **Instructor can / users cannot:**
    - Create a lesson
    - Create a lesson with the same name as another instructor (ie, 'Introduction Lesson')
    - Edit / Delete their own lessons

- **Instructor cannot:**
    - Create two lessons with the same name
    - Edit / Delete another instructors lessons

- **Superusers can**
    - View a list of user requests to become an instructor
    - Grand / Remove instructor status from users

## **Home Page**

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

## **Lessons Page**

1. **lessons view**
- **Valid requests**
    - Filters
        - When directed to the lesson page from the instructors page you are shown the instructor profile with their (sortable and filterable) lessons underneath.
        - Subscribed Lessons filter `/lessons/?filter=mylessons` only displays lessons currently subscribed to, or a message of "You are currently not subscribed to any lessons"
        - Purchased Lessons filter `/lessons/?filter=paidlessons` only displays purchased lessons, or a message "You have not purchased any lessons"
        - All Lessons filter `/lessons/?filter=None` displays all lessons

    - Stacked Filters
        - When viewing an instructors lessons
            - All lessons filter will only show lessons by that instructor as default
            - `/lessons/?filter=paidlessons` filter will only show lessons purchased from that instructor
            - `/lessons/?filter=mylessons` subscribed lessons filter will only show lessons subscribed to from that instructor


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

7. **review_lesson view**
- **Valid requests**
    - GET request will display a review form for the lesson or pre-fill the form with the existing review for editing
    - POST request will create a new review or update an existing review if available

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - User who passes an invalid lesson_id will be redirected home with the error "Cannot create/edit a review for an invalid lesson."
    - User who submits an invalid form are redirected back to the current lesson they were creating a review for with the error message "Error in review form: {form.errors}"
    - POSTs with an invalid rating out the range of 1-10 will be directed back to the lesson page with the error message "You entered an invalid rating, please try again."

8. **flag_review view**
- **Valid requests**
    - Request with a valid review.pk will create a flag for the review in question to be reviewd by an administrator, the user will be redirected back to the lesson page with a success message "{review.profile}'s review has been flagged and will be reviewed by an administrator soon")"

- **Error and Invalid request handling**
    - Users who pass an invalid review.pk will be taken back to the lesson page with an error message "Invalid review, please contact support if you think this is an error"
    - Users who try to flag a review multiple times will be taken back to the lesson page with the error message "{review.profile}'s review has been flagged and will be reviewed by an administrator soon")"

9. **delete_review view**
## **Profile Page**
- **Valid requests**
    - Request from a user will delete their review (and any associated flags against that review) and redirect them to the current lesson with a success message of "Review deleted"
    - Request from superuser in superuser_admin.html are handled by ajax and will delete the review (and any associated flags agains that review) and update request card without reloading with the message "Review deleted"

- **Error and Invalid request handling**
    - Superusers whos ajax request does not return {'success': 'True} are given the message in the request card "Error: Please check this item in djangos admin panel"
    - Users who submit a review to delete that does not exists are returned to the home page (as the lesson its self may be invalid now) and given the error message "Cannot delete review, review does not exist"
    - Users who submit a review to delete that does not belong to them are returned to the lesson page with the error message "Cannot delete review, it does not belong to this account."
    

- **Error and Invalid request handling**
    - Users who pass an invalid review.pk will be taken back to the lesson page with an error message "Invalid review, please contact support if you think this is an error"

1. **profile view**
- **Valid requests**
    - GET requests given a valid lesson_id will display a pre-filled lesson form ready for editing
    - POST requests will update a lesson with the new form data

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page

2. **edit_profile view**
- **Valid requests**
    - GET requests will render a template with a profile form `profiles/edit_profile.html`, pre-filled if any data exists on that profile
    - POST requests will update a profile with the new form data and return the user to their profile page (`profile` view)

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - User who submits invalid form will be redirected to the profile page with the error "There was an error in your profile data: {error}, please try again."

3. **instructors**
- **Valid requests**
    - Request will render a template with a card list of all instructors `profiles/instructors.html`

- **Error and Invalid request handling**
    - None needed

4. **request_instructor_status**
- **Valid requests**
    - If user profile is complete and status is "request" profile is updated to `profile.requested_instructor_status: True`
    - If user profile is complete and status is anything but "request" profile is updated to `profile.requested_instructor_status: False`

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - If user profile is not completed user is redirected back to profile page with the error message "You must complete your profile first."

## **Studio Page**

1. **studio view**
- **Valid requests**
    - Requests given a valid lesson_id will display the lesson if it is free or has been purchased

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - User who submits an invalid lesson_id will be redirected `home` with the error message "Error, Invalid lesson"
    - User who submits a paid lesson_id they have not purchased will be redirected `home` with the error message "You do not own this lesson"

## **Basket Page**

1. **view_basket**
- **Valid requests**
    - Renders `basket/basket.html` which shows all items currently in users basket (sessions)
    

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page


2. **add_to_basket**
- **Valid requests**
    - Adds an item to the session basket
    
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - Users who try a GET request are redirected to the home page with the error "Invalid request, please select lessons from the lessons page"
    - Users who post incorrect POST data are redirected to the home page with the error "Invalid request, please select lessons from the lessons page"
    - If a lesson_id is invalid users will be redirected to the home page with the error "Invalid lesson, please select lessons from the lessons page"

2. **remove_from_basket**
- **Valid requests**
    - Removed an item from the session basket
    
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - Users who POST invalid data/lesson_id are returned to the basket with the error "Invalid request, no lesson was specified for deletion"
    - If the removal fails for any other reason the user is returned to the basket with the error "Something went wrong, please contact {settings.DEFAULT_FROM_EMAIL} if you need assistance."

## **Checkout Page**

1. **checkout**
- **Valid requests**
    - GET request renders `checkout/checkout.html` with the checkout form and card payment option
    - POST request creates OrderForm and associated LineItems
    

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - GET:  Users who manually go to checkout with nothing in their basket are redirected home with the error message "Your basket is empty"
    - POST:  Users who submit an invalid basket are redirected back to the checkout page with the error "There was an error with your form, no charges have been made."
    - POST:  While the order form and its associated lineitems are being created, If a lesson does not exist they are warned of that on the checkout success page

2. **checkout_success**
- **Valid requests**
    - Renders `checkout/checkout_success.html` with confirmation of order and order details

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - Users who pass invalid order number are redirected home with the error message "This order was not found, please contact {settings.DEFAULT_FROM_EMAIL} for support."
    - Users who try to view someone elses order number through this view are given the error message "This order does not belong to this account, if this is an misake please contact {settings.DEFAULT_FROM_EMAIL} for support."

3. **attach_to_basket_intent**
- **Valid requests**
    - POST:  Sets up Stripe keys and adds metadata to Stripe payment intent

- **Error and Invalid request handling**
    - Users who are not logged in are redirected to signin page
    - Users who try to GET request this page are handled by the django @require_POST decorator
    - If the logic of this view fails, users are given the message "Sorry, your payment cannot be processed. please try again later. You have NOT been charged for this transaction."


## Solved Interesting Bugs
- **Instructor deletes lesson that is already a users basket**
- Situation - If an instructor deletes a lesson that is already in a users basket the user will receive a 404 error whenever the basket context processor is called because of this line `lesson = get_object_or_404(Lesson, lesson_id=lesson_id)`

- Task - Have the context processor handle lessons that have become invalid.

- Action - An `if` statemenet with djangos built in `.exists()` method checks to see if a lesson is still valid, if it is not the lesson_id is added to a list to be dealt with once the basket has been itterated through.  I did this as removing elements from a dictionary while itterating through it is a bad idea.  Once this is done lesson_ids in the invalid lessons list are popped off the basket session.

    - Code Before
    ```
    for lesson_id in basket:
    lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
    total += lesson.price
    product_count += 1
    basket_items.append({
        'lesson': lesson,
        'price': lesson.price,
    })
    basket_item_ids.append(lesson.lesson_id)
    ```

    - Code After
    ```
    for lesson_id in basket:
    # Check lesson_id is valid, remove from basket if not
    if not Lesson.objects.filter(lesson_id=lesson_id).exists():
        invalid_lessons_to_remove.append(lesson_id)
    # Add lesson to basket items
    else:
        lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
        total += lesson.price
        product_count += 1
        basket_items.append({
            'lesson': lesson,
            'price': lesson.price,
        })
        basket_item_ids.append(lesson.lesson_id)

    # Remove any invalid lessons
    if invalid_lessons_to_remove:
        for invalid_lesson in invalid_lessons_to_remove:
            basket.pop(invalid_lesson)
        invalid_lessons_to_remove = []
    ```

- **'Sort lesson by rating - high to low' feature had all non-rated lessons listed at the top**
- Situation - Code would show unrated lessons higher than rated lessons

- Task - Get unrated lessons to appear at the bottom of the sorted list

- Action - I used djangos F() expresson and nulls_last argument to sort null/None items to the bottom of the list, new code below
    - Code Before
    ```
    lessons = lessons.order_by(sortkey)
    ```
    - Code After
    ```
    if sort_direction == 'asc':
        lessons = lessons.order_by(F(sortkey).asc(nulls_last=True))
    else:
        lessons = lessons.order_by(F(sortkey).desc(nulls_last=True))
    ```
- Result - The lessons are now sorted correctly, though I cant append a simple tag `-` to reverse the sort direction so an if else statement is used instead

- **Anonymous users**
- Situation - A lot of features on this site require a user profile to function properly, catering to anonymous users involved a lot of code to `try:` getting the userprofile with `get_object_or_404` bloating code

- Task - Reduce this pattern in the code by following the DRY principle

- Action - I created a utility in the main app directory `yoga.utils.py` that contains a function that recieves a request and tries to get a profile from it or return `None`.
    - Code
    ```
    def get_profile_or_none(request):
    """ Function returns a valid UserProfile or None """
    try:
        return UserProfile.objects.get(user=request.user)
    except:
        return None
    ```

- Result - Any part of the app where it matters if a user is logged in or not will use a single line `get_profile_or_none(request)` to return a valid profile or a None object, reducing patterns in the code.

- **MEDIA_URL on a template no going through djangos interprator**

- Situation - Lesson modal Reviews and lesson description in the 'More Details' link are retrieved through a json response, this html is created from a template using render to string