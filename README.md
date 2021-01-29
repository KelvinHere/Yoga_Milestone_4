# Social Yoga - Full Stack - Milestone 4
 
This app allows users to sign up for simple yoga classes that instructors can make available.  
If the user likes the sample lesson, they can purchase futher/advanced lessons from the tutor.
The user will also have the ability to book personal video calls with the tutor for a fee.

* [Live link to site](#/ 'Heroku live link to app')
* [This Repository](https://github.com/KelvinHere/milestone-4 'Github repository link')

## ToDo
- add real email to allauth
instructor sorting
format accounts/confirm-email/
## Bugs
add to basket when navbar is collapsed shows on top left - move basket to collapsed nav
messages not showing color on topbar




## Contents
 
1. [**UX**](#ux)
   * [Project Purpose](#project-purpose)
   * [Wireframe Designs](#wireframe-designs)
   * [User Stories](#user-stories)
   * [Business Goals](#business-goals)
   * [Developer Goals](#developer-goals)
   * [Design Choices](#design-choices)   
       * [*General Design*](#general-design)
       * [*Colours and Fonts*](#colours-and-fonts)
2. [**Features**](#features)
   * [Existing Features](#existing-features)
       * [*Sorting*](#sorting)
       * [*Database*](#database)
       * [*Backend*](#backend)
       * [*Frontend*](#frontend)
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
        * [Deployment with Gunicorn](#deployment-with-gunicorn)
7. * [**Credits**](#credits)
       * [Content](#content)
       * [Media](#media)
       * [Acknowledgements](#acknowledgements)
 
## UX
 
#### Project Purpose

The purpose of this app is to create a platform where students can learn yoga remotely and
instructors can sell their lessons.  Users will be able to find an instructor and lessons 
through reviews and types of yoga, for a fee the user will be able to book video call time
through the website.


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

#### User Stories
As a site user I want to
1. Be able to register to the site to save my info for future use *
2. Quickly log in or out of the site *
3. Be able to recover my password

As a student user I want to
1. Have a free lesson to see if I like an instructor *
2. Find an instructor through reviews as I need to have some confidence before buying lessons
3. Learn yoga by watching videos
4. Get extra help with a lesson I am struggling with

As an Instructor I want to
1. Sell my services on this site to suppliment my income
2. Set the price of my services because I know what my time is worth
3. See a list of my booked times for video calls

As site admin I want to:
1. See requests from instructors
2. Change privilages for users and instructors
 
#### Business Goals

- RE: Students : the business purpose of this app is to engage the user with yoga lessons make money from selling lessons and video call time with instructors.

- RE: Instructors : make money from instructors by taking a cut of lessons and video calls sold.
 
 
#### Developer Goals
 
Each feature must be well programmed, function properly and tested to be bug free.
 
This project will display I have an understanding of full stack development from inception
to deployment.
 
To show an understanding of Django, Python, Postgres, Javascript, jQuery,
HTML, CSS, Gunicorn, Stripe payments and how they all interact to form a final product.
 
#### Design Choices

##### General Design

Bootstrap with cards is used to create and app that will be intuative to use.  The site will
keep a minimal clean look to keep information clear on smaller screens as this will be a responsive
mobile first app, allowing larger screens to show more 'cards' (lessons/insctructors) at once.

As the database of stuents and lessons grow, filtering and searching and subscribing to lessons/instructors
will be available.

Navigation and selection are consitent throughout the app.

##### Colours and Fonts
 
**Font 1**  - Quicksand (BOLD) is used for branding, titles, a strong font that is not completely serious lines up with the sytle and feel of the apps content.  Content text is displayed in a non bolded Quicksand.
 
**Font 2** - Poiret One is used for some smaller menu titles, ratings and subtitles.  A more delicate font that takes second seat to the more important information displayed in Quicksand.
 
**Colours** - Main colours of white (modern and clean) with blocks of medium brown (earth/nature) set the tone of mellow, natural and modern without resoring to garish colours.  Text will be brown on white or off-white on brown for consistancy.  The only strong colours are call to action and function buttons to help the user with the interface.  Any other colours will be light pastal.  All this will set the canvas for the instructor generated content and should not take away from their lesson and profile images.
 
## Features
 
### Existing Features

- User can:
    - Register / Sign In / Signout
    - Fill in a profile
        - Edit their profile
    - Request to become an instructor
    - Search available instructors
        - View instructors profile and lessons
    - Search available lessons
        - Subscribe to a lesson
        - Unsubscribe to a lesson
        - Start a lesson
        - Sort lessons by name / instructor / rating / price

- Instructor can:
    - Do anything a User can
    - Create a lesson
    - Delete a lesson
    - Edit a lesson

- Administrator can:
    - Do anythng a User can
    - View all requests to be an instructor
        - Accept / Reject that request
    - View a list of instructors
        - Remove the instructor priveliage

  
#### Sorting & Filtering

- If viewing lessons or instructors with a lesson list below
    - lessons can be sorted by
        - Rating ascending or descending
        - Lesson name ascending or descending
        - Instructor name ascending or descending
    - Lessons can be filtered by
        - All
        - Subscribed
        - Purchased

#### Database
 
 - The database is postgres, below is the final map, barring any development issues, of its construction.

![Database](https://github.com/KelvinHere/Yoga_Milestone_4/blob/master/design/database/db_design.jpg "Database design")


 
#### Backend

- Rating system
    - Situation: I wanted a rating system for lessons that would show the average score of all the reviews, but at scale for example 1000 lessons each had 100 reviews, everytime a user requested this list there would be 1000 x 100 = 100,000 objects in the queryset returned.
    - Task: To reduce the number of objects in the queryset needed to return the information requested by the user.
    - Action: After a review is created and saved it will call its lesson to run a method to update its average score.  This is only done when a review is created
    - Result: Now when a lesson list is called the average scores have been pre-calculated and only 100 objects in the queryset are returned as opposed to the theoretical 100,000
 
#### Frontend

- Any computation involving rating is performed in the backend

### Changes during development

### Future Features
 
##### Near Future
 
##### Far Future
 
## Testing
 
[Testing Documentation](#) - Documentation for testing

## Dependancies
- `pip3 install pillow` image field
- `pip install django_resized` resize image field

## Technologies Used
 
- **HTML5/CSS3**
- [Django](https://www.djangoproject.com/) - Framework
- [Postgresql](https://www.postgresql.org/) - Database
- [SQLite](https://www.sqlite.org/index.html) - Django default database
- [Python](https://www.python.org/) Programming language
- [Javascript](https://www.javascript.com/) Programming language
- [jQuery](https://jquery.com/) - JavaScript Library
- [Heroku](https://www.heroku.com/) - Cloud Application Platform
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server
- [Gitpod](https://www.gitpod.com) - Development environment
- [Git](https://git-scm.com/) - Version control
- [Github](https://www.github.com) - Code hosting platform
- [Draw.io](https://www.draw.io/) -Prototyping wireframing tool
- [Photoshop CS](https://www.adobe.com/) - Image editing software
 
## Deployment
 
This project was created in [GitPod](https://gitpod.io/) with the [Code Institute template](https://github.com/Code-Institute-Org/gitpod-full-template) and version controlled through 'Git', the project was committed and pushed to [GitHub](https://github.com/).
The project was then deployed to [Heroku](https://www.heroku.com/) with media and static files hosted on [Amazon s3](https://aws.amazon.com/).
 
### Version Control
* After files are created or modified they are committed to a GitHub repository using git by :-
    - adding the modified files locally using `git add .` or `git add filename.extension`
    - commiting the modified files with a message of changes using `git commit -m "changes here"`
    - pushing the new commit to the master branch on GitHub repository with `git push`
    - updating an out of date local branch with `git fetch origin` and pulling changes with `git pull origin`
 
### Local Deployment
  
### Heroku Deployment
 
The deployed version of 'Social Yoga' is hosted on Heroku and was deployed with the following steps.
 
* Requirements
    - A locally deployed version of the Book Review App from the instructions above
    - A Heroku account
    - A postgresql addon from Heroku > Resources
    - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed locally, instructions in [this link](https://devcenter.heroku.com/articles/heroku-cli)
 
1. Login to your Heroku account
2. Click New > App
3. Give the app a name, select a region and create the app

4. Setup the database
    4. The local app need 'dj_database_url' and 'psycopg2-binary' installing
    4. free requirements


4. Setup enviromental variables in Heroku :-
    - Select your app in Heroku and click settings
    - Under Config Vars set up the key value pairs as below
    - IP = 0.0.0.0
    - PORT = 5000
    - 
5. Login to Heroku from your terminal with `heroku login -i` then follow prompts
6. `pip freeze --local > requirements.txt` to update your requirements.txt in case of new requirements
7. `git init` if you have not initialised your git repo
8. `heroku git:remote -a YOUR_APP_NAME` to add remote
9. `git add .` and `git commit` your changes
10. `git push heroku master` to deploy to Heroku
11. From the Heroku website
    - You many need to click 'More' in the Heroku app and select 'Restart all dynos'
    - Click 'Open App' 
    - The App should now be running through Heroku
 
### Deployment with Gunicorn
 
As specified in the [Flask deployment](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment) documentation, Flasks built in server is not suitable for production as it does not scale well.
I decided to deploy to Heroku with Gunicorn as the server, deployment instructions on the Heroku website in [this link](https://devcenter.heroku.com/articles/python-gunicorn).
 
A quick summary of instructions with basic configuration below.
 
1. Locally install gunicorn with `pip install gunicorn`
2. `pip freeze --local > requirements.txt` to update your requirements.txt to include gunicorn
3. Create a point of entry for gunicorn, I created a file called [wsgi.py](https://github.com/KelvinHere/book-review-app/blob/master/wsgi.py) click to see its contents
4. Update the procfile to `web: gunicorn wsgi:app` so Heroku will launch the app through gunicorn
5. Log into heroku CLI and run `heroku config:set WEB_CONCURRENCY=3` to add an environmental variable into the app on heroku to take advantage of concurrency and make the app more responsive at scale
6. Commit your changes as before
7. Push to heroku with `git push heroku master`
8. The app should now be on heroku running on gunicorn
 
## Credits
### Content
 
- This project was created by KelvinHere
 
### Media

* [Background image](https://nicoledoherty.com/nd/wp-content/uploads/2012/11/credit-cards-you-trust-yourself.jpg)
* [simple_stretching.jpg and stretching descriptions](https://www.realsimple.com/health/fitness-exercise/stretching-yoga/stretching-exercises)
* [Instructor profile pictures from free images, contributor below](https://www.freeimages.com/)
    - [Instructor 1 - By Matteo Canessa](https://www.freeimages.com/photo/yoga-relax-1556603)
    - [Instructor 2 - By Aaron Neifer](https://www.freeimages.com/photo/yoga-1240391)
    - [Instructor 3 - By Lorant Fulop ](https://www.freeimages.com/photo/yoga-1433499)
    - [Instructor 4 - By Bimbo Cabochan](https://www.freeimages.com/photo/beach-yoga-1186865)
    - [Instructor 5 - By Martin Louis](https://www.freeimages.com/photo/yoga-1482810)
* [Drawn lesson poses](https://www.tummee.com/)
* [Lesson image poses prefixed self_](https://www.self.com/gallery/must-know-yoga-poses-for-beginners)
* [Yoga studio image](https://classpass.com/classes/space-yoga-studio-brighton?page=37)


### Acknowledgements
 
* [Geeks for Geeks - Ajax information](https://www.geeksforgeeks.org/handling-ajax-request-in-django/)
* [Django Documentation](https://docs.djangoproject.com/en/3.1/).
* [Code Institute](https://codeinstitute.net/).
* My mentor Spencer.
