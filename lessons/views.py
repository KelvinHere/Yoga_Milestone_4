from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import UserProfile
from lessons.models import Lesson, LessonItem

from .forms import LessonForm


def lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)
    all_lessons = Lesson.objects.all()
    
    # Get a list of subscribed lesson IDs for current user
    subscribed_lessons = LessonItem.objects.filter(user=profile)
    subscribed_lesson_list = []
    for each in subscribed_lessons:
        subscribed_lesson_list.append(each.lesson.lesson_id)

    template = 'lessons/lessons.html'
    context = {
        'profile': profile,
        'all_lessons': all_lessons,
        'subscribed_lesson_list': subscribed_lesson_list,
    }

    return render(request, template, context)


def my_lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'lessons/my_lessons.html'

    lessonItems = LessonItem.objects.filter(user=profile)

    context = {
        'profile': profile,
        'lessons': lessons,
        'lesson_items': lessonItems,
    }

    return render(request, template, context)


def instructor_created_lessons(request):
    """ View to return the lessons page """

    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'lessons/instructor_created_lessons.html'

    # Get lesson items bound to student
    instructor_created_lessons = Lesson.objects.filter(instructor_profile=profile)


    context = {
        'profile': profile,
        'instructor_created_lessons': instructor_created_lessons,
    }

    return render(request, template, context)


def subscribe_lesson(request, id):
    """ View to subscribe to a lesson """
    # Get needed fields
    profile = get_object_or_404(UserProfile, user=request.user)
    lesson = get_object_or_404(Lesson, pk=id)

    # Create LessonItem if it does not already exist
    if not LessonItem.objects.filter(lesson=lesson, user=profile).exists():
        LessonItem.objects.create(lesson=lesson, user=profile)

    return redirect('lessons')


def unsubscribe_lesson(request, id):
    """ View to remove a subscribed lesson from a UserProfile """
    unsubscribe = get_object_or_404(LessonItem, pk=id)

    unsubscribe.delete()
    return redirect('my_lessons')


def create_lesson(request):
    """ View to create a lesson """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Get form data
        lesson_name = request.POST.get('lesson_name')
        description = request.POST.get('description')
        url = request.POST.get('url')

        # Check for duplicate names
        instructor_created_lessons = Lesson.objects.filter(instructor_profile=profile).values_list('lesson_name', flat=True)

        if lesson_name not in instructor_created_lessons:
            # Create lesson
            Lesson.objects.create(instructor_profile=profile,
                                  lesson_name=lesson_name,
                                  description=description,
                                  url=url,
                                  )
        else:
            return HttpResponse('<h1>You already have a lesson named this<h1>', status=500)

    else:
        form = LessonForm(initial={'instructor_profile':profile})
        template = 'lessons/create_lesson.html'
        context = {
            'form': form
        }
        return render(request, template, context)


def delete_instructor_created_lesson(request, id):
    """ A view to delete a lesson given an id """
    profile = get_object_or_404(UserProfile, user=request.user)
    instructor_created_lesson = get_object_or_404(Lesson, lesson_id=id)

    if instructor_created_lesson.instructor_profile == profile:
        instructor_created_lesson.delete()
        return redirect('instructor_created_lessons')
    else:
        return HttpResponse('<h1>Error, this user did not create the lesson, please log in with the correct profile to delete it<h1>', status=500)

    
def edit_lesson(request, id):
    """ A view to edit and update a lesson """
    profile = get_object_or_404(UserProfile, user=request.user)
    instructor_created_lesson = get_object_or_404(Lesson, lesson_id=id)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=instructor_created_lesson)
        if form.is_valid():
            print('####valid')
            form.save()
        
        return redirect('instructor_created_lessons')

    else:
        form = LessonForm(instance=instructor_created_lesson)

        if instructor_created_lesson.instructor_profile == profile:
            template = 'lessons/edit_lesson.html'
            context = {
                'profile': profile,
                'lesson': instructor_created_lesson,
                'form': form,
            }
            return render(request, template, context)
        else:
            return HttpResponse('<h1>You can only edit your own lessons, check your login details and try again<h1>', status=500)