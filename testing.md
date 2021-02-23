# Testing Documentation for Social Yoga
!!!!!! Retest CSS validation after the last COLLECT STATIC!

1. [**Automated Testing**](#1---automated-testing)
   * [Unit Tests and Coverage](#unit-tests-and-coverage)
   * [Running unit tests](#running-unit-tests)
   * [Unit Test Results](#unit-test-results)
   * [Creating Unit Tests](#creating-unit-tests)
2. [**Manual Testing**](#2---manual-testing)
   * [Code Validation](#code-validation) 
        * [Browser Testing](#browser-testing)
        * [HTML Validation](#html-validation)
        * [CSS Validation](#css-validation)
        * [JavaScript Validation](#javascript-validation)
        * [Python Validation](#python-validation)
   * [Site Actions Tested](#site-actions-tested)
   * [Home Page](#home-page)
   * [Lessons Page](#lessons-page)
   * [Profile Page](#profile-page)
   * [Studio Page](#studio-page)
   * [Basket Page](#basket-page)
   * [Checkout Page](#checkout-page)
   * [Account Pages](#account-pages)
3. [**User Stories Solved**](#3---user-stories-solved)
4. [**Interesting Bugs Solved**](#4---interesting-bugs-solved)
 
## 1 - Automated Testing

### Unit Tests and Coverage
Automated testing is carried out by unit testing.  Coverage of these tests was monitored by 
using **Coverage** (`pip3 install coverage`), Coverage will create a report to show how much 
of the code is covered by the unit tests.

- Coverage can be run on individial apps like this `coverage run --source lessons manage.py test lessons`
    - I used the additional omit function when testing each individial app to remove migrations, see below for an example
    - `coverage run --omit=*/migrations/* --source lessons manage.py test lessons`
- The report from this can be viewed simply with `coverage report`
- Create an in depth report with visulisation of the code tested with `coverage html`
- View this indepth report by viewing **index.html** in the directory **htmlcov** in gitpod by
    - starting a http server `python3 -m http.server`
    - open the port and navigate to **htmlcov/index.html**


**Current Coverage Reports**

***

Home Coverage Report

![HomeCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/home.JPG "Home Coverage Report")

Missing from these tests are the custom 404 and 500 pages, these have been tested manually on the deployed app.

***

Profiles Coverage Report

![ProfilesCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/profiles.JPG "Profiles Coverage Report")

***

Basket Coverage Report

![BasketCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/basket.JPG "Basket Coverage Report")

***

Checkout Coverage Report

![CheckoutCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/checkout.JPG "Checkout Coverage Report")

Missing from these tests are the webhooks and webhook handlers, these have been tested on the deployed app and confirmed through stripe.

***

Sudio Coverage Report

![StudioCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/studio.JPG "Studio Coverage Report")

***

Lessons Coverage Report

![LessonsCoverage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/unittests/lessons.JPG "Lessons Coverage Report")


### Running unit tests
Create a local deployment as explained on ['Local Deployment' section of readme.md](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/README.md#local-deployment)

This apps unit tests use fixtures in the **profiles app**, for these to be loaded correctly the automatic creation of user profiles must be disabled, do this by setting `RUNNING_UNIT_TESTS` in settings.py to `True`

- To run all the tests - `python3 manage.py test`
- To run tests on an app, ie lessons app - `python3 manage.py test lessons`

You can keep narrowing the tests run like this, `python3 manage.py test lessons.tests.test_views.test_create_lesson` 

### Unit Test Results
![UnitTests](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/documents/tests/unit_tests_run_all.jpg "Unit Tests")

### Creating Unit Tests

- Follow [Running unit tests from the console](#running-unit-tests-from-the-console) to create a local deployment of the app.
- In settings.py set `RUNNING_UNIT_TESTS` to true, this will disable a view to allow fixtures to be loaded properly.
- Create your unit tests in the app you want to test for example lessons.tests.test_mynewtests.py
- Run the tests with `python3 manage.py test` to run the full test suite, or `python3 manage.py test lessons.tests.test_mynewtest` for just the example above.

## 2 - Manual Testing
***
### **Code Validation**
### Browser Testing
- This project has had all its pages, routes and responsive states viewed on the following browsers.
    - Chrome
    - Firefox
    - Edge
    - Opera

Read on to see all tests carried out on each page.

#### HTML Validation

- Live links below
    - [**Home Page** - Validation](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fms4-yoga-kelvinhere.herokuapp.com%2F#l295c39)
    - [**Sign in Page** - Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Fms4-yoga-kelvinhere.herokuapp.com%2Faccounts%2Flogin%2F)
    - [**Sign up Page** - Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Fms4-yoga-kelvinhere.herokuapp.com%2Faccounts%2Fsignup%2F)
    - [**Instructors Page** - Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Fms4-yoga-kelvinhere.herokuapp.com%2Fprofiles%2Finstructors%2F)
    - [**Lessons Page** - Validation](https://validator.w3.org/nu/?doc=https%3A%2F%2Fms4-yoga-kelvinhere.herokuapp.com%2Flessons%2F)

- Pages where login was required, these were input directly to the validator :-
    - Sign Out page - Validated
    - Create Lesson page - Validated
    - Profile page - Validated
    - Instructor Admin page - Validated
    - Superuser Admin page - Validated
    - Basket Page - Validated
    - Checkout Success Page - Validated
    - Checkout Page - Validated
        - 1 Error: "Empty H1", ignored as it is waiting for content from JavaScript

#### CSS Validation

CSS was validated through **W3C CSS Validation Service**.

- Live links below
    - [**base.css** - Validation](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fms4-yoga-kelvinhere.s3-eu-west-1.amazonaws.com%2Fstatic%2Fcss%2Fbase.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
    - [**checkout.css** - Validation](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fms4-yoga-kelvinhere.s3-eu-west-1.amazonaws.com%2Fstatic%2Fcheckout%2Fcss%2Fcheckout.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)

#### JavaScript Validation

The following files were validated through manually pasting the content into [beautifytools.com](https://beautifytools.com/javascript-validator.php) JavaScript validator.

- [stripe_elements.js](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/checkout/static/checkout/js/stripe_elements.js)
- [superuser_admin_js.html](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/home/templates/home/includes/superuser_admin_js.html)
- [delete_lesson_modal.js](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/lessons/static/lessons/js/delete_lesson_modal.js)
- [lesson_buttons.js](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/lessons/static/lessons/js/lesson_buttons.js)

#### Python Validation

The python code in this project was linted by using `python3 -m flake8`, this gives a list of lines that are non complient and a link to quickly access and correct them.
Some select lines were not corrected as it would make the code harder to read or break links.

The following errors remain.
- \<!DOCTYPE html> missing from some html files:  These were omitted from "includes" template files or files that extend from base to avoid getting HTML validation errors with out of place /<!DOCTYPE>'s through the final rendered pages.
- `./checkout/apps.py:8:9: F401 'checkout.signals' imported but unused` This sets up signals for checkout.signals.py.
- `./checkout/webhooks.py:43:80: E501 line too long (86 > 79 characters)` Left as not to break the payment intent line.
- Below, the AUTH_PASSWORD_VALIDATORS receive a line too long warning, these are setup up in the django file by default at this length, I have left them as is, the lines in question are below, with a quote from docs.djangoproject.com.
```
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""
From : https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

An exception to PEP 8 is our rules on line lengths. Don’t limit lines of 
code to 79 characters if it means the code looks significantly uglier or 
is harder to read. We allow up to 119 characters as this is the width of 
GitHub code review; anything longer requires horizontal scrolling which makes 
review more difficult. This check is included when you run flake8. 
Documentation, comments, and docstrings should be wrapped at 79 characters, 
even though PEP 8 suggests 72.
"""
```

## **Site Actions Tested**
- User can:
    - Register / Sign In / Signout / Confirm Email / Reset Password
    - View their profile
        - Edit their profile
        - Request to become an instructor
        - View a list of purchased lessons
    - Search available instructors
        - Sort these results by Name / Rating / Number of lessons available
    - View lessons
        - View 4 random, high rated, free, featured lessons on the homepage
        - By Instructor
        - Search lessons
        - Filter these results by All / Purchased / Subscribed
        - Sort these results by Name / Instructor / Rating / Price
            - All searching, sorting and filtering can be applied in any order and the results will stack
        - Subscribe / Unsubscribe to a lesson
        - Start a lesson that is free or they own
    - Buy lessons
        - Add a lesson they do not own to their basket
        - Remove a lesson from their basket
        - See the cost of each lesson and mini-description in their basket
        - See if they qualify for a discount
        - See a grand total
        - Checkout with Stripe
        - Start their lessons right from the checkout page
    - Review lessons
        - Create / Edit / Delete their reviews
        - Flag a review for administrator review
 
- Instructor can:
    - Do anything a User can
    - View a list of lessons they created
        - Create / Edit / Delete their lessons
    - View their sales
 
- Administrator can:
    - Do anything a User can
    - View all requests to be an instructor
        - Accept / Reject that request
    - View a list of instructors
        - Remove an instructors instructor privilege
    - View a list of flagged reviews
        - Ignore the flag or delete the review
 
## **Home Page**
 
- **Valid requests**
- While logged in, superusers can access "Superuser admin" where they can
    - Accept/reject users requests to become an instructor
    - Remove instructor status from an instructor
- Press the featured lessons button to display a cycling card of high rated, random, free lessons
 
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
    - Queries
        - `lessons/?q=`dog` only displays lessons with the word 'dog' in the lesson_name
 
    - Filters
        - When directed to the lesson page from the instructors page you are shown the instructor profile with their (sortable and filterable) lessons underneath.
        - Subscribed Lessons filter `/lessons/?filter=mylessons` only displays lessons currently subscribed to, or a message of "You are currently not subscribed to any lessons"
        - Purchased Lessons filter `/lessons/?filter=paidlessons` only displays purchased lessons, or a message "You have not purchased any lessons"
        - All Lessons filter `/lessons/?filter=None` displays all lessons
        - Accessed by the Instructors page `lessons/?instructor=VALID_INSTRUCTOR_ID` will display an instructor header with their searchable / sortable /filterable lessons underneath
    
    - Stacked filter/search/sort examples
        - `/lessons/?sort=rating&direction=asc&filter=mylessons&instructor=19&q=dog` 
            - will only show lessons user is subscribed to from that instructor with 'mountain' in the lesson name, sorted by rating in ascending order
        - `/lessons/?sort=price&direction=desc&filter=None&instructor=19&q=dog`
            - will only show paid lessons from that instructor that have 'dog' in the lesson name sorted by price in descending order
 
    - Pages, when next and previous buttons are pressed the user is taken to the next or previous page and any search/sort/filter parameters are kept
 
- **Error and Invalid request handling**
    - Queries
        - `/lessons/?q=` - A query with no term will return the error message "You did not enter any search query, please try again"
    - Filters
        - `/lessons/?filter=AN_INVALID_FILTER` - Invalid filters default to showing all lessons and will not return an error message
 
    - Sort direction
        - `lessons/?direction=INVALID_DIRECTION` - Invalid direction argument will default the sort to descending
        - `lessons/?sort=INVALID_SORT_ARGUMENT` - Invalid sort arguments will warn the user "Invalid sort value, displaying all lessons by name in ascending order"
 
    - Instructor
        - `lessons/?instructor=NOT_AN_INSTRUCTOR` Passed a user that is not an instructor, user redirected to instructors page error message "This user is not an instructor, please pick one from the instructor list."
        - `lessons/?instructor=INVALID_USER` Passed a user that does not exist, user redirected to instructor page with error message "This instructor was not found, please pick one from the instructor list."
    
    - Pages
        - If the user changes filters/sorting/search parameters when on a page other than one, they are taken back to page one using the new parameters
        - If the user presses next on the last page, or previous on the first, they are kept on the same page they are currently on
        - If the user manually enters a page number that does not exist in the address bar they are taken back to page 1 with the error message "Page does not exist, returning to page 1"
 
2. **subscribe view**
- **Valid Requests**
    - When passed a valid lesson_id along with
        - `subscribe=true` the user is subscribed to the lesson and JS updates the buttons from "Subscribe" to "Unsubscribe" and "Sart Lesson"
        - `subscribe=false` the user is unsubscribed to the lessons and JS updates the buttons from "Unsubscribed" and "Start Lesson" to "Subscribe"
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - Trying to submit an invalid lesson_id `/lessons/subscriptions/?subscribe=true&lesson_id=INVALID_LESSON_ID` returns user to lessons page with the error message "Invalid request, no lessons have been subscribed or unsubscribed to."
    - Trying to alter subscription status of a lesson using something other than `true` or `false` returns the user to lessons page and gives the error message "Invalid request, no lessons have been subscribed or unsubscribed to."
    - A nonsense request with invalid GET keys passed returns the user to the lesson page with an error message "Invalid request, no lessons have been subscribed or unsubscribed to."
 
3. **instructor_admin view**
- **Valid requests**
    - Lessons tab displays a list of lessons the logged in instructor has created or a prompt "You have not created any lessons yet"
    - Sales tab displays a list of lessons bought from this instructor with price, lesson name, buyer, date and price before and after the sales percentage (at time of sale) is removed.
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - If user is not an instructor they are returned to the homepage with the error message "Only instructors can do this"
 
4. **delete_lesson view**
- **Valid requests**
    - If an instructor passes a valid lesson_id and the logged in profile matches the profile of the lesson creator, the lesson is delete_lesson
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to pass the lesson_id from a lesson they did not create they are given the error message "This lesson does not belong to you and has not been deleted, please check your username and try again."
    - If an instructor tries to pass an invalid lesson_id they are given the error message "Invalid lesson ID, no lessons were deleted."
    - Instructors cannot delete a lesson that has been purchased by customers, they can only edit it, the delete button is disabled and gives the reason why.
    - If an instructor tries to delete by manually submitting the lesson_id to the view they are redirected to the instructor_admin page and given the error message "You cannot delete a lesson customers have purchased."
 
5. **create_lesson view**
- **Valid requests**
    - GET request will display a lesson creation form to the user
    - POST request will create a lesson from the form data and return the user to their created lesson list
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to create a lesson with the same name as one of their existing lessons they are directed back to their created lessons page with the error message "You already have a lesson named this."
        - Regarding duplicate names, different instructors can have lessons with the same name to avoid "reserving" of popular names such as simple yoga poses, ie both 'Benny' and 'Charle' can have a lesson named 'Mountain Pose'
 
 
6. **edit_lesson view**
- **Valid requests**
    - GET requests given a valid lesson_id will display a pre-filled lesson form ready for editing
    - POST requests will update a lesson with the new form data
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - If a user who is not an instructor tries to access this view they are directed to the home page with the error "Only instructors can do this."
    - If an instructor tries to POST data to an invalid lesson_id they are redirected to their created lessons page with the error message "Invalid lesson ID, no lessons were updated."
    - if an instructor tries to GET another instructors lesson_id they are redirected to their created lessons page with the error message "You can only edit your own lessons, please check your username."
 
7. **review_lesson view**
- **Valid requests**
    - GET request will display a review form for the lesson or pre-fill the form with the existing review for editing
    - POST request will create a new review or update an existing review if available
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - User who passes an invalid lesson_id will be redirected home with the error "Cannot create/edit a review for an invalid lesson."
    - User who submits an invalid form are redirected back to the current lesson they were creating a review for with the error message "Error in review form: {form.errors}"
    - POSTs with an invalid rating out the range of 1-10 will be directed back to the lesson page with the error message "You entered an invalid rating, please try again."
    - Users cannot create reviews on their own lessons, they are returned to the lesson page with the error "You cannot review your own lessons."
 
8. **flag_review view**
- **Valid requests**
    - Request with a valid review.pk will create a flag for the review in question to be reviewed by an administrator, the user will be redirected back to the lesson page with a success message "{review.profile}'s review has been flagged and will be reviewed by an administrator soon")"
 
- **Error and Invalid request handling**
    - Users who pass an invalid review.pk will be taken back to the lesson page with an error message "Invalid review, please contact support if you think this is an error"
    - Users who try to flag a review multiple times will be taken back to the lesson page with the error message "{review.profile}'s review has been flagged and will be reviewed by an administrator soon")"
 
9. **delete_review view**
- **Valid requests**
    - Given a review primary key the review will be deleted and the user directed back to the studio page they were on.
    - Activated from superuser admin, review will be deleted and admin will stay on the same page jquery will remove the review div.
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - User who passes an invalid review primary key will be redirected home with the error "Cannot delete review, review not found."
    - Users who submit a primary key that is not theirs (barring superusers who do have this authority) will be directed back to the lesson page with the error message "Cannot delete review, it does not belong to this account."
 
## **Profile Page**
- **Valid requests**
    - Request from a user will delete their review (and any associated flags against that review) and redirect them to the current lesson with a success message of "Review deleted"
    - Request from superuser in superuser_admin.html are handled by ajax and will delete the review (and any associated flags against that review) and update request card without reloading with the message "Review deleted"
 
- **Error and Invalid request handling**
    - Superusers whos ajax request does not return {'success': 'True} are given the message in the request card "Error: Please check this item in django's admin panel"
    - Users who submit a review to delete that does not exists are returned to the home page (as the lesson itself may be invalid now) and given the error message "Cannot delete review, review does not exist"
    - Users who submit a review to delete that does not belong to them are returned to the lesson page with the error message "Cannot delete review, it does not belong to this account."
    
 
- **Error and Invalid request handling**
    - Users who pass an invalid review.pk will be taken back to the lesson page with an error message "Invalid review, please contact support if you think this is an error"
 
1. **profile view**
- **Valid requests**
    - GET requests given a valid lesson_id will display a pre-filled lesson form ready for editing
    - POST requests will update a lesson with the new form data
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
 
2. **edit_profile view**
- **Valid requests**
    - GET requests will render a template with a profile form `profiles/edit_profile.html`, pre-filled if any data exists on that profile
    - POST requests will update a profile with the new form data and return the user to their profile page (`profile` view)
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - User who submits invalid form will be redirected to the profile page with the error "There was an error in your profile data: {error}, please try again."
 
3. **instructors**
- **Valid requests**
    - Request will render a template with a card list of all instructors `profiles/instructors.html`
    - `profiles/instructors/?sort_by=rating&sort_direction=desc` will display instructors by rating in descending order
    - `profiles/instructors/?q=ben` will only show instructors with "ben" in their username
    - `profiles/instructors/?sort_by=rating&sort_direction=desc&q=ben` will only show instructors with "ben" in their username by rating in descending order
 
- **Error and Invalid request handling**
    - Entering an invalid sort will redirect the user back to the instructor page with the error message "Invalid sort value displaying all instructors by rating in descending order"
    - Invalid sort direction will default to descending order
    - Passing an empty query will redirect the user back to the instructors page with the error message "You did not enter any search query, please try again"
 
4. **request_instructor_status**
- **Valid requests**
    - If user profile is complete and status is "request" profile is updated to `profile.requested_instructor_status: True`
    - If user profile is complete and status is anything but "request" profile is updated to `profile.requested_instructor_status: False`
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - If the user profile is not completed, the user is redirected back to the profile page with the error message "You must complete your profile first."
 
## **Studio Page**
 
1. **studio view**
- **Valid requests**
    - Requests given a valid lesson_id will display the lesson if it is free or has been purchased
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - User who submits an invalid lesson_id will be redirected `home` with the error message "Error, Invalid lesson"
    - User who submits a paid lesson_id they have not purchased will be redirected `home` with the error message "You do not own this lesson"
 
## **Basket Page**
 
1. **view_basket**
- **Valid requests**
    - Renders `basket/basket.html` which shows all items currently in users basket (sessions)
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
 
2. **add_to_basket**
- **Valid requests**
    - Adds an item to the session basket
    
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - Users who try a GET request are redirected to the home page with the error "Invalid request, please select lessons from the lessons page"
    - Users who post incorrect POST data are redirected to the home page with the error "Invalid request, please select lessons from the lessons page"
    - If a lesson_id is invalid users will be redirected to the home page with the error "Invalid lesson, please select lessons from the lessons page"
 
2. **remove_from_basket**
- **Valid requests**
    - Removed an item from the session basket
    
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - Users who POST invalid data/lesson_id are returned to the basket with the error "Invalid request, no lesson was specified for deletion"
 
## **Checkout Page**
 
1. **checkout**
- **Valid requests**
    - GET: Request renders `checkout/checkout.html` with the checkout form and card payment option
    - POST: Request with correct field entries and card details creates an OrderForm and associated LineItems
    - STRIPE: When processing the order, when stripe returns a patmentIntent.status = succeeded, the order form will be submit to the checkout view and the cusotmer will have access to their purchases (see checkout success below).
    - On a complete order an email is sent with an order confirmation to the email input on the checkout page.
    
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - GET:  Users who manually go to checkout with nothing in their basket are redirected home with the error message "Your basket is empty"
    - POST:  Users who submit an invalid basket are redirected back to the checkout page with the error "There was an error with your form, no charges have been made."
    - POST:  While the order form and its associated lineitems are being created, If a lesson does not exist they are warned of that on the checkout success page
    - STRIPE: Invalid card details fetch stripe error messages and display them below the card field
    - STRIPE: If the user closes the browser or there is an issue before the app receives the STRIPE paymentIntent, the OrderForm will not be created, but the checkout.webhook_handler.py will listen for the stripe webhook and create the OrderForm there instead.
    
 
2. **checkout_success**
- **Valid requests**
    - Renders `checkout/checkout_success.html` with confirmation of order and order details
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - Users who pass invalid order numbers are redirected home with the error message "This order was not found, please contact {settings.DEFAULT_FROM_EMAIL} for support."
    - Users who try to view someone else's order number through this view are given the error message "This order does not belong to this account, if this is a mistake please contact {settings.DEFAULT_FROM_EMAIL} for support."
 
3. **attach_basket_to_intent**
- **Valid requests**
    - POST:  Sets up Stripe keys and adds metadata to Stripe payment intent
 
- **Error and Invalid request handling**
    - Users who are not logged in are redirected to sign in page
    - Users who try to GET request this page are handled by the django @require_POST decorator
    - If the logic of this view fails, users are given the message "Sorry, your payment cannot be processed. please try again later. You have NOT been charged for this transaction."

4. **webhooks**
- **Valid requests**
    - Checkout page creates a payment intent and if that succeeds 
    !!!!!! Do more here
- **Error handling**
    - If user closes the browser or the order form is not submitted via JavaScript, the backend will look for the orderform for 5 times over 5 seconds, if still not found the Order will be created in the webhook.

## **Account Pages**

- **Valid requests**
    - User logging in with correct details is logged in and receives a success message
    - User logging out is logged out
    - User signing up with valid details will have an account created and a validation email setting
    - Validation emails contain a link that activate the account
    - Reset password will send a reset password email to the accounts email

- **Error and Invalid request handling**
    - Invalid details will not let a user log in
    - Incorrectly input form data will display an error message on the form
 
## 3 - User Stories Solved
***
**ID** | **As A/AN** | **I want to be able to...** | **So that I can** | **Outcome**
--- | --- | --- | --- | ---
1 | Site User | Register to the site | Have a personalised experience | **User can register**
2 | " | Quickly Login/Out | To access my subscriptions and purchases | **Login/Out buttons in nav or collapsed nav**
3 | " | Recover/Reset my password | Get back into my account when I forget it | **Oauth recover password sends recovery link**
4 | " | View my personal profile | Set up a bio and view all my purchases | **User has profile page, with purchases on it**
6 | Student | View a list of instructors | Read about them to find one I like | **Instructors link on nav gives list of instructors**
5 | " | Search / sort and filter lessons | Get to the ones I want Quickly | **Query/Sort/Filter available on lessons, Query/Sort available on instructors**
7 | " | View reviews on lessons | To make sure they are worth my time | **Reviews viewable from lesson cards and inside lesson**
8 | " | Try free lessons | To make sure I like an instructor before buying for them | **Students can view free lessons**
9 | " | Buy lessons | Get premium content and support an instructor I like | **Students can buy paid lessons**
10 | " | Write/Edit/Delete a lesson review | show how much I liked or disliked it | **Users can write review on free lessons or lessons they own**
11 | " | Flag a review | Report inappropriate content | **Logged in users can flag a review via icon on the review**
12 | Instructor | Create free lessons | Get students interested in me | **Instructors can make free lessons**
13 | " | Create paid lessons and price them | Earn some money for my time | **Instructors can create and price paid lessons**
14 | " | Edit / Delete my lessons | Remove a lesson or mistakes from one | **Instructors can use instructor admin page to perform these tasks**
15 | " | View lesson sales | To see my earnings and how well a lesson is performing | **Instructors can view their sales in instructor admin page**
16 | Administrator | See requests from instructors | Vet them and grant/reject them instructor status | **Superuser Admin page displays these requests with appropriate action buttons**
17 | " | Remove instructor status from an instructor | remove instructors that break rules or are inactive | **Superuser Admin page can display all instructors with appropriate action button**
18 | " | View flagged comments | Decide to remove the review if it is inappropriate | **Superuser Admin page displays these flags with appropriate action buttons**
 
 
## 4 - Interesting Bugs Solved
***
- **Instructor deletes lesson that is already a users basket**
- Situation - If an instructor deletes a lesson that is already in a users basket the user will receive a 404 error whenever the basket context processor is called because the lesson no longer exists in the database but its ID is still in the users basket.
 
- Task - Have the basket context processor handle lessons that have become invalid.
 
- Action - Use djangos built in `.exists()` method to check if a lessons in the basket are still valid, if it is not the case the lesson_id is added to a removal list to be dealt with once the basket has been iterated through.  I did this as removing elements from a list or dictionary while iterating through it is a bad idea.  Once this is done lesson_ids in the invalid lessons list are popped off the basket session.
 
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

- Result - The lesson is removed from the basket before the user can get a 404 error.
***
- **'Sort lesson by rating - high to low' feature had all non-rated lessons listed at the top**
- Situation - Code would show unrated lessons higher than rated lessons
 
- Task - Get unrated lessons to appear at the bottom of the sorted list
 
- Action - I used django's F() expression and nulls_last argument to sort null/None items to the bottom of the list, new code below
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
- Result - The lessons are now sorted correctly, though I can't append a simple tag `-` to reverse the sort direction so an if else statement is used instead
 ***
- **Anonymous users**
- Situation - A lot of features on this site require a user profile to function properly, catering to anonymous users involved a lot of code to `try:` getting the user profile with `get_object_or_404` bloating code
 
- Task - Reduce this pattern in the code by following the DRY principle
 
- Action - I created a utility in the main app directory `yoga.utils.py` that contains a function that receives a request and tries to get a profile from it or return `None`.
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
 ***
- **MEDIA_URL on a template no going through django's interpreter**
 
- Situation - 'Lesson modal' content reviews and lesson description are retrieved through a json response, this html string is created from a template using render to string, when being created the {{ MEDIA_URL }} is not rendered into the string, giving the wrong url to the default_profile_image.jpg
 
- Task - Get the MEDIA_URL to be correctly represented in the string
 
- Action - Just before the modal is rendered to string, a variable `MEDIA_URL_for_json = settings.MEDIA_URL` is also passed as context to the render_to_string method
 
- Result - The correct MEDIA_URL location is rendered into the string without having to hard code a location in the template.
***
- **404 error creating a 500 internal server error on deployed project**

- Situation - When deployed, testing for a 404 error page by giving an invalid URL.  I was receiving a 500 internal server error rather than the expected 404 error, with debugging turned off I had not enought information to figure out the problem.

- Task - Find out what was causing the 500 server error with debugging turned off.

- Action -  The django documentation on [Logging](https://docs.djangoproject.com/en/3.1/topics/logging/) gives examples of loggers, I used these to get more information on the 500 error I was getting by creating a logger and viewing the results of these logs through logging into Heroku in the console and running `heroku log -t` which would then give much more information.
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}
```

- Result - Given the extra log information I was able to find the source of the 500 internal server error and correct it, the logging can now be activated by adding an enviromental EXTRA_LOGGING variable if needed.
***
- **No CSRF Token in static js file**
 
- Situation - When moving my lesson buttons JavaScript to a static file my Ajax POST request was giving a Forbidden error because of a missing CSRF Token as the token was initially rendered into the script by a template tag.
 
- Task - Get the CSRF Token to my JavaScript function
 
- Action - In lessons.html, just before I include the static JavaScript file I created a small script to declare the CSRF Token variable so it is available for the JavaScript in my static file.
```
<script>
        // Define csrf token for static js file below
        let csrfToken = '{{ csrf_token }}';
    </script>
```
- Result - The static file now has access to the CSRF Token again and the buttons function correctly
