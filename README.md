# Social Yoga - Full Stack - Milestone 4
 
The idea of this app is to create a space where people can learn yoga from a multitude of instructors.
 
Users can sign up and find lessons that instructors have created, free or paid.  Users can find out 
about these lessons through descriptions / reviews and ratings and decide if they would like to subscribe
or buy them.
Instructors who decide to use this site will be able to create and manage their lessons through the apps
tools, set lesson prices and view the details of all the sales they have made on the site.
 
 
* [Live link to site](https://ms4-yoga-kelvinhere.herokuapp.com/ 'Live website link')
* [This Repository](https://github.com/KelvinHere/milestone-4 'Github repository link')
 
## ToDo
contact email and social media links
image change on forms
make a JS carousel on the front page from random lessons
 
## Bugs
Error on stripe checkout when checking out on deployed version
 
## Contents
 
1. [**UX**](#ux)
   * [Project Purpose](#project-purpose)
   * [Wireframe Designs](#wireframe-designs)
   * [User Stories](#user-stories)
   * [Database](#database)
   * [Business Goals](#business-goals)
   * [Developer Goals](#developer-goals)
   * [Design Choices](#design-choices)   
       * [*General Design*](#general-design)
       * [*Colours and Fonts*](#colours-and-fonts)
2. [**Features**](#features)
   * [Quick Feature Breakdown](#quick-feature-breakdown)
   * [NavBar Features](#navbar-features)
   * [Instructors Page Features](#instructors-page-features)
   * [Instructor Admin Page Features](#instructor-admin-page-features)
   * [Lessons Page Features](#lessons-page-features)
   * [Studio Page Features](#studio-page-features)
   * [Profile Page Features](#profile-page-features)
   * [Basket Page Features](#basket-page-features)
   * [Checkout Success Page Features](#checkout-success-page-features)
   * [Performance](#performance)
   * [Feature Changes During Development](#feature-changes-during-development)
   * [Future Features](#future-features)
       * [*Near Future*](#near-future)
       * [*Far Future*](#far-future)
3. * [**Changes during Development**](#changes-during-development)
4. * [**Testing**](#testing)
5. * [**Technologies Used**](#technologies-used)
6. * [**Deployment**](#deployment)
        * [Version Control](#version-control)
        * [Local Deployment](#local-deployment)
        * [Heroku Deployment](#heroku-deployment)
        * [Differences - Local & deployed](#differences---local-and-deployed)
7. * [**Credits**](#credits)
       * [Content](#content)
       * [Media](#media)
       * [Acknowledgements](#acknowledgements)
 
## UX
 
#### Project Purpose
 
The purpose of this app is to create a platform where students can learn Yoga remotely and
instructors can create and sell lessons.  Users will be able to find an instructor and lessons 
through search and filtering options, then view ratings on instructors and reviews/ratings on
lessons.  The store for this app is built around instructor generated content, the idea being
after a while it could potentially grow itself.
 
It will offer instructors set of tools to easily create and manage their lessons, adjust prices,
lesson content and cultivate through quality lessons, good reviews, ratings and a following of
students to sell their premium lessons to.
 
#### Wireframe Designs
 
- The home page
![HomePage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/wireframe/1-Index.jpg "Home page")
- Signup / Register / Logout page
![AccountsPage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/wireframe/2-Login_Out.jpg "Login / out / signup page")
- Sortable list of instructors on the site
![InstructorsPage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/wireframe/3-Instructors.jpg "Instructors page")
- An instructors page, includes profile and all lessons with ability to subscribe or buy
![InstructorPage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/wireframe/4-Instructor.jpg "Instructor page")
- A typical lesson page, paid or free
![LessonPage](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/wireframe/5-Lesson.jpg "Lesson page")
 
### Database
 
 - For the app I used a postgres relational database, below is the final map with all features included.
 
![Database](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/database/db_design.jpg "Database design")
 
#### User Stories
 
**ID** | **As A/AN** | **I want to be able to...** | **So that I can**
--- | --- | --- | ---
1 | Site User | Register to the site | Have a personalised experience 
2 | " | Quickly Login/Out | To access my subscriptions and purchases
3 | " | Recover/Reset my password | Get back into my account when I forget it
4 | " | View my personal profile | Set up a bio and view all my purchases
6 | Student | View a list of instructors | Read about them to find one I like
5 | " | Search / sort and filter lessons | Get to the ones I want Quickly
7 | " | View reviews on lessons | To make sure they are worth my time
8 | " | Try free lessons | To make sure I like an instructor before buying for them
9 | " | Buy lessons | Get premium content and support an instructor I like
10 | " | Write/Edit/Delete a lesson review | show how much I liked or disliked it
11 | " | Flag a review | Report inappropriate content
12 | Instructor | Create free lessons | Get students interested in me
13 | " | Create paid lessons and price them | Earn some money for my time
14 | " | Edit / Delete my lessons | Remove a lesson or mistakes from one
15 | " | View lesson sales | To see my earnings and how well a lesson is performing
16 | Administrator | See requests from instructors | Vet them and grant/reject them instructor status
17 | " | Remove instructor status from an instructor | remove instructors that break rules or are inactive
18 | " | View flagged comments | Decide to remove the review if it is inappropriate
 
#### Developer Goals
 
Each feature must be well programmed, function properly and tested to be bug free.
 
This project will display I have an understanding of full stack development from inception
to deployment, giving a good showcase project for a portfolio.
 
Show an understanding of Django, Python, Postgres, Javascript, jQuery,
HTML, CSS, Gunicorn, Stripe payments and more, and how they all interact to form a final product.
 
#### Design Choices
 
##### General Design
 
Bootstrap is my chosen framework to create the app as it is quick to style pages in a familiar way.  It will follow 
common design principles so it will be familiar and intuitive to use.  The site will keep a minimal clean look to keep 
information clear on smaller screens as this will be a responsive mobile first app.
 
To allow this site to scale when the database of instructors and lessons grow; filtering, searching, sorting and subscribing
lessons & searching for instructors is available.
 
Navigation and selection will be consistent throughout the app, with no need to use the browser back button.
 
##### Colours and Fonts
 
**Font 1**  - Lato is used for branding, titles, a strong font that is not completely serious lines up with the style 
and feel of this app.
 
**Font 2** - Quicksand is used for content.  A more delicate font that takes second seat to the more important 
information displayed in Lato.
 
**Colours** - Main colours of white (modern and clean) with blocks of medium brown (earth/nature) set the tone as 
mellow, natural and modern without resorting to garish colours.  Text will be natural brown on white or off-white on brown for 
consistency.  The only strong colours are call to action and function buttons to help the user navigate the interface.  All
this will be a canvas for the instructor generated content and it should not take away from their lesson and profile images
and content which will become the heart of the app.
 
## Features
 
### Quick feature breakdown
 
A quick review of features on the site, more detailed descriptions further down.
 
- User can:
    - Register / Sign In / Signout / Confirm Email / Reset Password
    - View their profile
        - Edit their profile
        - Request to become an instructor
        - View a list of purchased lessons
    - Search available instructors
        - Sort these results by Name / Rating / Number of lessons available
    - View lessons
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
 
### NavBar Features
 
The nav bar appears on every page, it is locked to the top on larger screens and can be scrolled away on smaller screens.  The basket will display how many
items it has inside.  Each time the navbar is loaded it uses a variable in a context processor in the checkout app called `product_count`, which allows the navbar
to always have the information needed, this context processor is documented in the 
[Solved Interesting Bugs](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/testing.md#solved-interesting-bugs) section of testing.md as an interesting 
case "Instructor deletes lesson that is already a users basket".
 
- Logo Brand is always a link home.
- Navbar expands from burger button on larger screens.
- If logged in basket is always on the navbar and never collapses.
- basket has "+n" where n is equal to the number of items in it.
- 'Instructors' link takes user to a list of instructors to choose from.
- If logged in, 'Lessons' dropdown gives a choice of All / Subscribed / Purchased lessons.
- 'Account' link is personalised if the user is logged in and has the following options.
    - Logged out: Register / Sign In
    - Logged in:
        - User: My Profile / Logout
        - Instructor: Instructor Admin / My Profile / Logout
        - Administrator: Superuser Admin / My Profile / Logout
 
### Home Page Features
 
The page is responsive and the buttons and background image reposition between mobile, tablet, desktop 
screens to always look pleasing.
 
- The website's main text is personalised if the user is logged in.
- Button: "Find an Instructor" appears if the user is not logged in or is not currently subscribed to any lessons.
- Button: "Your subscribed lessons" call to action button appears if the user is logged in to push engagement.
- Button: "Instructor admin" call to action button appears if the user is an Instructor to promote engagement.
- Personalised Toast to show login success in an unobtrusive position.
 
 
### Superuser_admin Page Features
 
Allows an administrator to quickly and easily deal with user requests, review flags and privileges without using the django /admin page.
It consists of three tabs, Requests / All Instructors / Flagged.
 
The page is responsive, the tabs are collapsed to a vertical arrangement on mobile and horizontal on larger screens.
 
- Requests Tab:
    - **Functionality**
    - Users who have requested to become instructors through their profile will show here.
    - This tab title will display the current amount of user requests using a styled red icon, ie 'Requests **+2**'.
    - Each card under this shows the user's profile and **email link** so an administrator can easily contact, vet them and decide to 'Accept' of 'Reject' the request by the buttons below the request.
    - If accepted the user is granted instructor status which gives access to the Instructor Admin page to create / edit / delete lessons.  The request is then removed from the superuser_admin page.
    - If rejected the user's request is set back to standard user and the request is removed from the superuser_admin page.
    - **Responsiveness**
    - The user request changes layout between small and large screens for easier viewing.
 
- All Instructors Tab:
    - **Functionality**
    - This tab displays a list of all current instructors.
    - A button to remove instructor status is on each instructor if needed.
    - **Responsiveness**
    - Items change layout from small to larger screens for easier viewing.
 
- Flagged Tab:
    - **Functionality**
    - This tab displays a list of flagged reviews.
    - Like the Requests Tab, this tab shows a red **+n** icon next to the tab to alert admins something needs attention.
    - The flagged review cards show:
        - Who created the review
        - The lesson it was created for
        - The review content
        - A **list** of people who flagged the review
        - An 'Ignore' button if the review is fine
        - A 'Remove Review' button to remove the review from the database
    - `LessonReviewFlagged` is the model used to handle flags:
        - It contains two foreign key fields `Profile` of the user who flagged the review and `LessonReview` the actual review.
        - If a flag is ignored all entries of `LessonReviewFlagged` that contain the `LessonReview` in question are deleted to save the administrator having to delete them individually or them staying redundantly in the database forever.
        - If a `LessonReview` is deleted all entries of `lessonReviewFlagged` that contain the foreign key `LessonReview` are removed as the field is set to on_delete=models.CASCADE.
    - **Responsiveness**
    - None needed
 
### Instructors Page Features
 
This page gives the user a list of instructors, by default they are sorted by rating high to low.
 
- **Functionality**
- Instructors can be searched by name or partial name.
- Instructors can be sorted by Rating / Name / Number of lessons available.
- Sorting can be stacked with searching.
- The user can press the "Enter Studio" button to get more information about an instructor and a list of their lessons to start / subscribe / buy.
    - With this "studio page" the user can filter, sort **and** query the passed instructors lessons.
- **Responsiveness**
- On small screens the instructor card is vertically stacked with a small profile image.
- Larger screens the card is laid out horizontally with a larger profile image.
 
### Instructor Admin Page Features
 
Through tabs the instructor can view Created Lessons / Sales / Support.  They can create, delete and edit lessons, view a list of sales from their paid lessons and have access to support information.
 
- **Functionality**
    - Lessons Tab:
        - lessons are sorted by date added, newest first.
        - 'Create lesson' allows an instructor to make a new lesson.
        - 'Edit' button allows the user to edit a lesson.
        - 'Delete' button allows an instructor to delete a lesson as long as no one has bought it.
        - After lesson is created the lesson finds out how many lessons were made by this instructor can passes it to the instructor profile method `_update_lesson_count()`
        - After lesson is deleted, the a method is called in the instructors `UserProfile` to update the amount of lessons they have created
        - Instructor can't make two lessons with the same name
        - Instructor can make a lesson with the same name as another instructor to prevent 'name reserving'
    - Sales Tab:  Displays all sales this instructor has made.
    - Support Tab:  Displays the sites current contact email.
- **Responsiveness**
- On small screens the lesson card is vertically stacked with a small profile image.
- Larger screens, the lesson card is laid out horizontally with a larger profile image.
- The sales and flag cards reorder content for easier viewing over screen sizes.
 
### Lessons Page Features
 
This page shows a list of lessons using pagination, they can be searched, filtered and sorted.
 
To save on repeat code (DRY principle) the 'instructor studio' uses this lessons page with an 'instructor_profile_header' snippet activated by context to display instructor information over their filtered lessons.
 
- **Searching / Sorting / Filtering**
- Lessons can be searched, filtered and sorted
    - Filter by All / Subscribed / Purchased
        - A tick shows which filter is currently applied
    - Sort by Rating / Name / Price / Instructor Name
        - All sorting can be reversed
    - Searched by name / partial name
        - Search query can be dismissed by auto generated button on page
    - All these features stack and whatever order these features are applied no previous search / filter or sort information is lost.
 
- Example of a complex search:  Search the instructor **'Sophia'** from the instructors page & search lesson name **'dog'** & filter by **subscribed** & sort by **rating descending**
    - This would return Lessons you are subscribed to, made by 'Sophia' that contain 'dog' in the lesson name and will be sorted by highest rating first.
 
- **Pagination**
    - Pagination saves long loading times and scrollbars by distributing large lists of lessons into pages.
    - Next and Previous buttons take user to next and previous page of lessons while keeping filter/search/sort parameters
 
**Lesson cards**
A lesson card contains all lesson information and context sensitive buttons.
- **Buttons**
    - Logged out users:-
        - A call to action button "Signup to view" on the lesson card encourages the user to join the site and directs them to the Signup page so they can view the lesson.
    - Logged in users :-
        - Paid Lessons that are non purchased will show an add to basket button ie "€5.99" with an add to basket icon, if the discount threshold is reached the discount top-bar is replaced by JS with a discount reached top-bar.
            - Clicking the buy lesson button adds the lesson to the basket, uses JS to change the button to "Added" , creates a popover on the basket saying "Your lesson has been added to the basket" and adds +1 to the basket icon on the navbar.
            - Clicking the button "Added" uses JS to create a popover saying "You have already added this to your basket".
        - Lessons that are free or purchased that are not subscribed to show a red "Subscribe to lesson" button.
            - Clicking the 'Subscribe to lesson' replaces that button using JS to the 'Unsubscribe' and 'Start Lesson' buttons.
        - Lessons that are subscribed to show an Unsubscribe and Start Lesson button.
            - Clicking 'Unsubscribe' replaces itself and the 'Start Lesson' button using JS with the 'Subscribe' button.
            - Clicking 'Start Lesson' starts the lesson.
- **Dynamic**
    - The rating score is an average of all the reviews the lesson has, if there are no reviews the lesson says Rating: None so the user knows it is not an awful 0 rated lesson.
    - Paid lessons that have been purchased have their price changed to a green "Purchased" to inform the user is one of their purchased lessons.
    - On mobile the lesson cards are vertically stacked with a small image.
    - On larger screens the cards are laid out horizontally with a larger image.
- **Modal**
    - The More Details link uses Ajax to POST a csrf token and lesson_id to the get_modal_data view, if the request is valid, the view will return json data.
    - The json data contains a status key and a modal that is inserted into the page and activated with jQuery.
    - This modal contains the lesson information with a longer description of the lesson and all of its reviews.
    - The modal is created by using render_to_string on a snippet called lesson_modal.html that is given the context 'lesson instance' and 'MEDIA_URL_for_json' as it will not be parsed the same as a standard rendered template.
 
### Studio page Features
 
This is the page where the actual lesson happens, it has the lesson name, the embedded video, a dropdown for description and reviews underneath.
 
- **Functionality**
    - Embedded lesson video can be viewed on this page.
    - Users who try to access a paid lesson but don't own it will be refused access with an error message "You do not own this lesson".
    - A description button displays a collapsed description of the lesson.
    - If no current user review exists a 'Write review' button is displayed which takes the user to a form to write a review and give it a score 0-10.
    - If a current user review exists that review will be displayed at the top of the reviews with an edit and delete icon to perform those actions.
    - If no reviews exist (discounting the current user) a prompt of "No more reviews exist" is displayed.
    - If other reviews exist they will be displayed in date order (newest first).
    - If a user is viewing their own lesson the "Write Review" button is removed as users cannot review their own lessons.
    - Flag icon
        - Reviews that do not belong to the logged in user have a flag icon to allow them to be reported to an administrator.
        - Administrators can see all flagged reviews on the superuser_admin.html (/home/superuser_admin view)page.
        - If a user flags a review they will receive a success message "{{ User }}'s review has been flagged and will be reviewed by an administrator soon.".
        - If a user tries to flag a review more than once they will receive the error message "You have already flagged {{ User }}'s review it will be reviewed by an administrator soon.".
 
### Profile Page Features
 
The profile page shows users their profiles, lets them edit it and request to become an instructor.  A list of purchased lessons and buttons to start them are also on this page for quick access.
 
- **Functionality**
- An 'Edit Profile' button takes the user to a form where they can edit their profile information and change their picture.
- When pressed, the 'Request Instructor Status' button :-
    - Will put a flag on the Userprofile that they want to be an instructor, this request can be seen by administrators on superuser_admin.html and change the users button via JS to "Under Review: Press to cancel".  Their profile status will change to "Under review".
    - Pressing "Under Review: Press to cancel" removes the flag and cancels the request.
    - If the user has not finished their user profile will be prompted by toast "Error, you must complete your profile first."
    - If the user's request is granted the 'Under Review: Press to cancel' button is disabled changed to the success color and displays "Instructor Status Granted", the users profile status is changed to "Instructor" and they will now have access to the 'Instructor Admin' page.
- **Responsiveness**
- On small screens the instructor profile is vertically stacked with a small profile image and purchased lessons underneath.
- Larger screens the instructor profile is laid out horizontally with a larger profile image and purchased lessons underneath.
 
### Basket Page Features
 
The basket page shows cards of items added to the basket with image, title, instructor, price and a delete button.
The Total, any discount and grand total are shown with a prompt of how much more they need to spend to avail of a discount if they have not reached that amount yet.
Finally a checkout button at the bottom of this information.
 
- **Functionality**
    - A button styled as a red trash can icon will remove the item from the basket and update the basket product count and adjust prices.
    - The checkout button will take the user to the checkout page ready for card payment.
- **Responsiveness**
    - The table resizes itself to fit nicely on any size screen over 300px wide.
 
### Checkout Page Features
 
The checkout page displays the total that will be charged to the user and how many items they are buying.  For example "Total: €8.99 \ For 2 items"
A form asks for a full name and email-address where a confirmation email will be sent, and a card number.
 
- **Functionality**
    - Email address has to be valid format.
    - Card details are checked on the fly and any error message from invalid input is displayed below.
    - 'Complete order' button starts the process of placing the order through Stripe and unlocking the lesson for the user.
    - See 'checkout testing' in testing.md for information on webhooks used to validate an order.
    - A 'Back to basket' button takes the user back to their basket.
    - If an order fails to process the user is given the error message that the order failed and they were not charged.
    - If lessons cannot be found while processing the order they will be removed from the transaction.
- **Responsiveness**
    - On larger screens the checkout window sits on top of a blurred yoga studio image as there is little information on this screen and having it all white was too jarring.
    - On smaller screens the checkout window takes the full screen.
 
### Checkout Success Page Features
 
The checkout success page tells the user their order was successful and gives them their order information of, name, email, order number, total, discount if applicable.
Also a list of all lessons ordered with buttons to start them.
 
- **Functionality**
    - Using django signals each lesson item that is purchased will automatically create a subscription for that lesson so the user can find it easily and start it right away.
    - "Begin" button on each bought lesson item will start that purchased lesson.
- **Responsiveness**
    - On larger screens the checkout window sits on top of a blurred yoga studio image as there is little information on this screen and having it all white was too jarring.
    - On smaller screens the checkout window takes the full screen.
 
Regarding signals, if for any reason an `OrderLineItem` (the database entry that shows a lesson has been purchased by a user) is or has to be deleted, a `signal` (pre_delete) is used to delete the subscriptions the user may have for the lesson.
 
### Performance
 
- This app has been written with performance in mind, to try and only access the database when necessary and to make the queries and model access as lightweight as possible, below is an example.
 
- Rating system
    - Situation: I wanted a rating system for Instructors and Lessons that would show the average score of each instructor by lessons and each lesson by their reviews, but at scale for example 1000 lessons each had 100 reviews, everytime a user would request a list of all lessons there would be 1000 x 100 = 100,000 objects in the queryset returned to get all the review ratings.
    - Task: To reduce the number of objects in the queryset needed to return the information requested by the user.
    - Action: After a review is created and saved it will call its lesson to run a method to update its average score.  This is only done when a review is created, once the lesson rating is updated it will call the Instructor that created it to run a method that updates their score from all their (precalculated) lesson ratings.
    - Result: Now when a lesson list is called the average scores have been pre-calculated and in this example only 100 objects in the queryset are returned as opposed to 100,000
 
### Feature Changes during development
As this was a learning project some changes were made in development to get the most out of it.  Most notably I changed 
a "book video time" feature with a "paid lesson" feature.  This allowed me to make a more comprehensive "store", and create
a system where once a lesson is paid for is is unlocked for the user, showing another example of defensive programming in
case of a user trying to access a lesson they do not own.
 
The lesson and instructor layout was changed from initially having more than one lesson or instructor per row on larger screens
to just having one per row.  As there is robust sorting and filtering in the project it made more sense to maintain the order
of the results than to cram more results onto a single page, this combined with pagination makes results easier to read and follow.
 
The database was changed over the course of the project as I added more interesting features to the app, such as the rating
cascading rating system and review / review flagging system.
 
### Future Features
 
In making this app, there are ideas I would like to implement at a later date that are beyond the scope and deadline of this
project, they are listed below.
 
##### Near Future
- Implement a time limit on uploading images so a user cannot spam images to the application.
- Use a private video hosting service to give the site more control and better security for paid lessons (sharing of urls).
- Ignore users flags feature, will allow an administrator to ignore flags created by a user in case they misuse this feature.
- Create an "on sale" field on the lessons model so instructors can have their on sale lessons promoted on the homepage.
    - Check lesson was on at a normal price for at least 2 months
    - When taken off sale cannot be put back on sale for at least 2 months to avoid spamming sales to reach the front page.
 
##### Far Future
- Create live-streaming paid lessons, where an instructor can sell limited positions to join realtime lessons with direct tutor feedback.
 
## Testing
 
[Testing Documentation](#) - Documentation for testing
 
## Technologies Used
 
- **HTML5/CSS3**
- [Django](https://www.djangoproject.com/) - Framework to create the app
- [Heroku](https://www.heroku.com/) - Cloud Application Platform to deploy the app to 
- [Postgres](https://www.postgresql.org/) - Database to keep track of the apps data
- [SQLite](https://www.sqlite.org/index.html) - Django default database for local development
- [Python](https://www.python.org/) Programming language to write the backend
- [Javascript](https://www.javascript.com/) Programming language for the frontend
- [jQuery](https://jquery.com/) - JavaScript Library to simplify DOM manipulation
- [AWS S3](https://aws.amazon.com/) - Cloud Storage Host to keep static and media files for the app
- [Stripe](https://stripe.com/en-ie) - Online payment processing to process the apps store transactions
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP web server for the app
- [Gitpod](https://www.gitpod.com) - Development environment
- [Git](https://git-scm.com/) - Version control
- [Github](https://www.github.com) - Code hosting platform
- [Draw.io](https://www.draw.io/) -Prototyping wireframing tool
- [Photoshop CS](https://www.adobe.com/) - Image editing software
- [Django_resized](https://pypi.org/project/django-resized/) - To resize images to a specified size
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for python, to configure AWS features
- [Botocore](https://github.com/boto/botocore) - Boto3's low-level core functionality
- [DJ Database URL](https://pypi.org/project/dj-database-url/) - Django utility to support multiple databases, including PostgreSQL used in this app
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) - An integrated set of Django applications that deal with authentication / registration and account management + more.
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Django utility that lets you control the rendering behaviour of django forms
- [django-storages](https://github.com/jschneier/django-storages) - A collection of custom storage backends for Django
- [Pillow](https://github.com/python-pillow/Pillow/blob/fcc42e0d344146ee9d265d1f43c094ce5a0ec4cf/docs/index.rst) - Pillow adds image processing capabilities to the Python interpreter.
- [psycopg2-binary](https://www.psycopg.org/) - A PostgreSQL adapter for python it will convert database data into python lists.
- [s3transfer](https://pypi.org/project/s3transfer/) - A python library for managing S3 transfers
 
## Deployment
 
This project was created in [GitPod](https://gitpod.io/) with the [Code Institute template](https://github.com/Code-Institute-Org/gitpod-full-template) and version controlled through 'Git', the project was committed and pushed to [GitHub](https://github.com/).
The project was then deployed to [Heroku](https://www.heroku.com/) with media and static files hosted on [Amazon s3](https://aws.amazon.com/).
 
### Version Control
* After files are created or modified they are committed to a GitHub repository using git by :-
    - adding the modified files locally using `git add .` or `git add filename.extension`
    - commiting the modified files with a message of changes using `git commit -m "changes here"`
    - pushing the new commit to the master branch on GitHub repository with `git push`
    - updating an out of date local branch with `git fetch origin` and pulling changes with `git pull origin`
 
* Branches & an example
    - When adding the pagination feature I created a new `branch` on github, this allowed me to experiment with pagination without breaking my master branch and having to do a hard reset back to a working commit.
    - Once the feature was working in the `Add pagination branch` I created a `pull request` to `merge` this new branch back into the `master`, since the master branch was a couple of `commits` ahead at this point I had to confirm there were no `conflicts` and I was happy to go ahead with this operation.
    - With the merge complete the master branch now contains the pagination feature and the commits in the master branch that were ahead of my `Add pagination branch` at the time.
 
### Local Deployment
 
* Requirements
    - Local computer with an IDE, Python 3.8.6, git and pip.
 
Clone this repository to your local workspace :-
 
1. Open the [Yoga_Milestone_4](https://github.com/KelvinHere/Yoga_Milestone_4) repository.
2. Click the 'Code' button and then copy the 'Clone with HTTPS' URL.
3. From your IDE open a terminal.
4. From inside the directory you want the clone, type `git clone` and paste the URL you copied from GitHub then press enter.  Example below.
    - `git clone https://github.com/KelvinHere/Yoga_Milestone_4.git`
 
5. Cloning will be completed when your terminal is waiting for its next command.
6. More information or changes in the cloning procedure at this link [Git Clone](https://github.com/git-guides/git-clone).
7. Make sure pip is up to date `pip install --upgrade pip`
8. Install the app requirements `pip install -r requirements.txt`
10. Run `python3 manage.py runserver` to start the app
11. Open the given link in your IDE and the app will be ready to use.
 
### Heroku Deployment
 
The deployed version of 'Social Yoga' is hosted on Heroku and can be deployed with the following steps.
 
* Requirements
    - A locally deployed version of the Book Review App from the instructions above
    - A Heroku account
    - A postgresql addon from Heroku > Resources
    - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed locally, instructions in [this link](https://devcenter.heroku.com/articles/heroku-cli)
 
1. Login to your Heroku account
2. Click New > App
3. Give the app a name, select a region and create the app
 
4. Setup the database
    - In Heroku > Resources, search for `Heroku Postgres` and add this addon
    - Make sure the postgres `DATABASE_URL` config var has been set in Heroku > Settings > ConfigVars
 
5. Setup a Django secret key
    - Use an online generator such as [Miniwebtool](https://miniwebtool.com/django-secret-key-generator/) to create a new secret key
    - Add this as a Heroku enviromental variable under settings as
        - SECRET_KEY
 
6. Setup Cloud Storage
    - Setup a cloud storage provider such as Amazon AWS S3 / Google cloud / Backblaze by following their instructions to set up a bucket, example below
    - [AWS Setup Example](https://docs.aws.amazon.com/quickstarts/latest/s3backup/step-1-create-bucket.html)
    - Retrieve and add the keys as heroku envorimental variables
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - USE_AWS = True (Without this the app will default to using a local database)
    - Copy the media files from the local project to the bucket while keeping the same directory structure
 
7. Setup Stripe payments
    - Create a stripe account
    - In Stripe > Developers > API keys get the publishable and secret key, add these as Heroku enviromental Vars
        - STRIPE_PUBLIC_KEY
        - STRIPE_SECRET_KEY
    - In Stripe > Developers > webhooks, add a new endpoint
        - Endpoint URL = The url in Heroku > Settings > Domain
        - Select receive all events under "Events to send"
        - Add endpoint
    - Open this new endpoint and get the `Signing Secret` add this as a Heroku enviromental var
        - STRIPE_WH_SECRET
    - Now the app should connect to Stripe and be able to receive webhooks from it.
 
8. Setup Emails for the app :-
    - Gmail example
    - In All setting > Accounts and Import > Other google settings > Security turn on 2 factor authentication
    - Select the newly available option "App Passwords" and follow login instructions
    - Under select app chose `Other` and give it a name
    - Press generate and copy the app password then setup up the following Heroku enviromental vars
        - EMAIL_HOST_PASS = The password just generated
        - EMAIL_HOST_USER = The gmail email
    - Django should now be able to send emails through this address.
    
9. Login to Heroku from your terminal with `heroku login -i` then follow prompts
10. `pip freeze --local > requirements.txt` to update your requirements.txt in case of new requirements
11. `git init` if you have not initialised your git repo
12. `heroku git:remote -a YOUR_APP_NAME` to add remote
13. `git add .` and `git commit` your changes
14. `git push heroku master` to deploy to Heroku
15. During the build all static files should be uploaded to the connected AWS bucket, to stop this happening every build add the Heroku enviromental var `DISABLE_COLLECTSTATIC=1`
16. From the Heroku website
    - You many need to click 'More' in the Heroku app and select 'Restart all dynos'
    - Click 'Open App' 
    - The App should now be running through Heroku
 
### Differences - Local and deployed
 
- !!!!!!!!!!! Code and env vars to switch between dev and deployment
 
## Credits
 
- [Code](https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield) - Films answer: For testing an imagefield without an image
- [Colour scheme inspired by icolorpalette](https://icolorpalette.com/palette-by-themes/yoga) - How to create an image without an image file for testing image fields in forms in tests. `small_gif = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b')`
- [Generated Photos](https://generated.photos/) - AI generated Student Faces used for student profiles
 
 
### Content
 
- This project was created by KelvinHere
 
### Media
 
* [Background image](https://www.istockphoto.com/photo/young-woman-practicing-yoga-in-the-nature-female-happiness-pose-balance-body-vital-gm1221748282-358248235?clarity=false)
* [simple_stretching.jpg and stretching descriptions](https://www.realsimple.com/health/fitness-exercise/stretching-yoga/stretching-exercises)
* [Instructor profile pictures from free images, contributor below](https://www.freeimages.com/)
    - [Instructor 1 - By Matteo Canessa](https://www.freeimages.com/photo/yoga-relax-1556603)
    - [Instructor 2 - By Aaron Neifer](https://www.freeimages.com/photo/yoga-1240391)
    - [Instructor 3 - By Lorant Fulop ](https://www.freeimages.com/photo/yoga-1433499)
    - [Instructor 4 - By Bimbo Cabochan](https://www.freeimages.com/photo/beach-yoga-1186865)
    - [Instructor 5 - By Martin Louis](https://www.freeimages.com/photo/yoga-1482810)
* [Drawn lesson poses](https://www.tummee.com/)
* [Lesson image poses 'self'](https://www.self.com/gallery/must-know-yoga-poses-for-beginners)
* [Yoga studio image on account and checkout pages](https://classpass.com/classes/space-yoga-studio-brighton?page=37)
* [Sun salutation image](https://www.ladylair.net/yoga-sun-salutation-poses/)
* [Yoga Pose Clipart](http://clipart-library.com/images/kcMK47bXi.jpg)
* [Illustrated Pose Images](https://www.sheknows.com/health-and-wellness/articles/1020135/12-basic-yoga-poses-for-beginners/)
 
 
### Acknowledgements
 
* [Geeks for Geeks - Ajax information](https://www.geeksforgeeks.org/handling-ajax-request-in-django/)
* [Django Documentation](https://docs.djangoproject.com/en/3.1/).
* [Code Institute](https://codeinstitute.net/).
* My mentor Spencer.
 