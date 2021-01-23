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

