# Social Yoga - Full Stack - Milestone 4
 
This app allows users to sign up for simple yoga classes that instructors can make available.  
If the user likes the sample lesson, they can purchase futher/advanced lessons from the tutor.
The user will also have the ability to book personal video calls with the tutor for a fee.

* [Live link to site](#/ 'Heroku live link to app')
* [This Repository](https://github.com/KelvinHere/milestone-4 'Github repository link')
 
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
 
- The home
![HomePage](# "Book view wireframe image")
- Lessons can be browsed
![LessonPage](# "Book view revealed wireframe image")
- Buy time with instructor
![InstructorPage](# "View reviews wireframe image")
- Merchandise
![MerchangisePage](# "Form wireframe image")
 
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
 
##### Colours and Fonts
 
**Font 1**
 
**Font 2**
 
**Colours**
 
## Features
 
### Existing Features
  
#### Sorting
 
#### Database
 
#### Backend
 
#### Frontend
 
### Changes during development

### Future Features
 
##### Near Future
 
##### Far Future
 
## Testing
 
[Testing Documentation](#) - Documentation for testing

## Dependancies
- `pip3 install pillow` image field

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
 
* Requirements
    - An Atlas MongoDB account with a database called `book_app_db` which has the collections `books` and `genres`
    - An Atlas user profile called `root` with read/write access to the `book_app_db` database
    - Local computer with an IDE, Python 3.8.6, git and pip.
 
Clone this repository to your local workspace :-
 
1. Open the [Book Review App](https://github.com/KelvinHere/book-review-app) repository.
2. Click the 'Code' button and then copy the 'Clone with HTTPS' URL.
3. From your IDE open a terminal.
4. From inside the directory you want the clone, type `git clone` and paste the URL you copied from GitHub then press enter.  Example below.
 
- `git clone https://github.com/KelvinHere/book-review-app.git`
 
5. Cloning will be completed when your terminal is waiting for its next command.
6. More information or changes in the cloning procedure at this link [Git Clone](https://github.com/git-guides/git-clone).
7. Make sure pip is up to date `pip install --upgrade pip`
8. Install the app requirements `pip install -r requirements.txt`
9. Link the app to your Atlas MongoDb account through an environment variable
    - Login to Atlas MongoDb
    - Click Clusters > Overview > Connect
    - Click 'connect your application'
    - Select your driver and version ie 'Python' '3.6 or later'
    - Copy the given "Connection String"
    - Create env.py in the root of the local book app workspace and add the code below
        - `import os`
        - `os.environ.setdefault("MONGO_URI", )`
    - Paste the Connection String inside os.environ.setdefault() and replace the <> markers with your Atlas details
    - The contents of env.py should look similar to the code below
        - `import os`
        - `os.environ.setdefault("MONGO_URI", "mongodb+srv://root:MYPASSWORD@firstcluster.er9ib.mongodb.net/book_app_db?retryWrites=true&w=majority")`
10. Run `python3 app.py` to start the app
11. Open the given link in your IDE and you will be connected to your Atlas book_app_db and can start adding books.
 
 
### Heroku Deployment
 
The deployed version of 'Book Review' is hosted on Heroku and was deployed with the following steps.
 
* Requirements
    - A locally deployed version of the Book Review App from the instructions above
    - A Heroku account
    - [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed locally, instructions in [this link](https://devcenter.heroku.com/articles/heroku-cli)
 
1. Login to your Heroku account
2. Click New > App
3. Give the app a name, select a region and create the app
4. Setup enviromental variables in Heroku :-
    - Select your app in Heroku and click settings
    - Under Config Vars set up the key value pairs as below
    - IP = 0.0.0.0
    - PORT = 5000
    - MONGO_URI = The Atlas MongoDb Connection String as explained in [local deployment](#local-deployment) above
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

### Acknowledgements
 
* [Geeks for Geeks - Ajax information](https://www.geeksforgeeks.org/handling-ajax-request-in-django/)
* [Django Documentation](https://docs.djangoproject.com/en/3.1/).
* [Code Institute](https://codeinstitute.net/).
* My mentor Spencer.
