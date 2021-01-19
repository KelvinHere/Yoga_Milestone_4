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

 - Sort lesson by rating has all non-rated lessons at the top

 - Problem - code would show unrated at top
    - `lessons = lessons.order_by(sortkey)`

- Solution - Use djangos F() expresson and nulls_last to sort null items to bottom
    - `if sort_direction == 'asc':`
    - `lessons = lessons.order_by(F(sortkey).asc(nulls_last=True))`
    - `else:`
    - `lessons = lessons.order_by(F(sortkey).desc(nulls_last=True))`

- Problem 2 - Original code changed the direction of the sort by prepending `-` onto the sortkey

- Solution 2 - An if else statement replaces this functionality to change the sort direction