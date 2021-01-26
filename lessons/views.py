from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User
from lessons.models import Lesson, LessonItem, LessonReview
from checkout.models import OrderLineItem
import json

from yoga.utils import get_profile_or_none

from .forms import LessonForm, ReviewForm


def lessons(request):
    """ View to return the lessons page """
    profile = get_profile_or_none(request)
    sortkey = 'lesson_name'  # Default sort parameter
    direction = None
    sort_direction = 'asc'
    lesson_filter = None
    page_title = 'All Lessons'
    sub_title = None
    filter_title = 'All Lessons'
    instructor_to_display = None
    subscribed_lesson_list = []
    paid_lesson_list = None
    valid_sort_values = ['name', 'instructor', 'rating', 'price']

    lessons = Lesson.objects.all()

    if request.GET:
        # Sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey not in valid_sort_values:
                messages.error(request, 'Invalid sort value, displaying all lessons by name in ascending order')
                return redirect(reverse('lessons'))

            if sortkey == 'name':
                sortkey = 'lesson_name'
            if sortkey == 'instructor':
                sortkey = 'instructor_profile'
            if sortkey == 'rating':
                sortkey = 'rating'
            if sortkey == 'price':
                sortkey = 'price'

        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sort_direction = 'desc'

        # Filtering
        if 'filter' in request.GET:
            if request.GET['filter'] == 'mylessons':
                lesson_filter = 'mylessons'
            if request.GET['filter'] == 'paidlessons':
                lesson_filter = 'paidlessons'

        # Instructor header
        if 'instructor' in request.GET:
            if request.GET['instructor']:
                instructor_id = request.GET['instructor']
                instructor_to_display = get_object_or_404(UserProfile, id=instructor_id)
                page_title = f"Welcome to {instructor_to_display}'s Studio"
                lessons = lessons.filter(instructor_profile=instructor_to_display)

    # If authenticated
    if request.user.is_authenticated:
    
        # Get a list of subscribed lesson IDs for current user
        subscribed_lessons = LessonItem.objects.filter(user=profile)
        for subscribed_lesson in subscribed_lessons:
            subscribed_lesson_list.append(subscribed_lesson.lesson.lesson_id)

        # Get a list of paid lessons
        paid_lessons = OrderLineItem.objects.filter(profile=profile)
        paid_lesson_list = []
        for paid_lesson in paid_lessons:
            paid_lesson_list.append(paid_lesson.lesson.lesson_id)

    # Apply any filters and set up redirect reverse for buttons and page title
    if lesson_filter:
        if lesson_filter == 'mylessons':
            lessons = lessons.filter(lesson_id__in=subscribed_lesson_list)
            if not lessons:
                sub_title = 'You are currently not subscribed to any lessons'
            page_title = 'Subscribed Lessons'
            filter_title = page_title

        if lesson_filter == "paidlessons":
            if paid_lesson_list:
                lessons = lessons.filter(lesson_id__in=paid_lesson_list)
                if lessons:
                    page_title = 'Purchased Lessons'
            else:
                lessons = lessons.filter(lesson_id__in=paid_lesson_list)
                page_title = 'Purchased Lessons'
                sub_title = 'You have not purchased any lessons'
            filter_title = 'Purchaed Lessons'
        
        # If viewing an instructor and also filtering
        if instructor_to_display:
            page_title = f"Welcome to {instructor_to_display}'s Studio"

    # Sort
    if sort_direction == 'asc':
        lessons = lessons.order_by(F(sortkey).asc(nulls_last=True))
    else:
        lessons = lessons.order_by(F(sortkey).desc(nulls_last=True))

    # Create template and context
    template = 'lessons/lessons.html'
    context = {
        'profile': profile,
        'all_lessons': lessons,
        'subscribed_lesson_list': subscribed_lesson_list,
        'paid_lesson_list': paid_lesson_list,
        'page_title': page_title,
        'sub_title': sub_title,
        'filter_title': filter_title,
        'current_filter': lesson_filter,
        'instructor_to_display': instructor_to_display
    }

    return render(request, template, context)


@login_required
def subscriptions(request):
    """ View to remove a subscribed lesson from a UserProfile """
    if request.method == 'GET':
        lesson_id = request.GET['lesson_id']
        profile = get_object_or_404(UserProfile, user=request.user)
        lesson_object = Lesson.objects.get(lesson_id=lesson_id)        

        if request.GET['subscribe'] == 'false':
            unsubscribe = LessonItem.objects.filter(lesson=lesson_object, user=profile)
            unsubscribe.delete()
            json_response = json.dumps({'subscription_status': 'unsubscribed'})
            return HttpResponse(json_response, content_type='application/json')

        elif request.GET['subscribe'] == 'true':
            if not LessonItem.objects.filter(lesson=lesson_object, user=profile).exists():
                LessonItem.objects.create(lesson=lesson_object, user=profile)
            json_response = json.dumps({'subscription_status': 'subscribed'})
            return HttpResponse(json_response, content_type='application/json')

        else:
            return HttpResponse('<h1>Something went wrong, no lessons have been subscribed or unsubscribed to.</h1>', status=500)


@login_required
def instructor_created_lessons(request):
    """ View admin for lessons instructors have created """

    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'lessons/instructor_created_lessons.html'

    # Get lesson items bound to student
    instructor_created_lessons = Lesson.objects.filter(instructor_profile=profile)

    context = {
        'profile': profile,
        'instructor_created_lessons': instructor_created_lessons,
    }

    return render(request, template, context)


@login_required
def delete_instructor_created_lesson(request, id):
    """ A view to delete a lesson given an id for instructor created lessons """
    profile = get_object_or_404(UserProfile, user=request.user)
    instructor_created_lesson = get_object_or_404(Lesson, lesson_id=id)

    if instructor_created_lesson.instructor_profile == profile:
        instructor_created_lesson.delete()
        return redirect('instructor_created_lessons')
    else:
        return HttpResponse('<h1>Error, this user did not create the lesson, please log in with the correct profile to delete it<h1>', status=500)


@login_required
def create_lesson(request):
    """ View to create an instructor lesson """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Get lesson name form data
        lesson_name = request.POST.get('lesson_name')

        # Check for duplicate names
        instructor_created_lessons = Lesson.objects.filter(instructor_profile=profile).values_list('lesson_name', flat=True)

        if lesson_name not in instructor_created_lessons:
            # Create lesson
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)  # Delay commit of form to enter profile on next line
                lesson.instructor_profile = profile
                lesson.save()
                return redirect('instructor_created_lessons')
            return redirect('instructor_created_lessons')
        else:
            return HttpResponse('<h1>You already have a lesson named this<h1>', status=500)

    else:
        form = LessonForm(initial={'instructor_profile':profile})  # Insert current user in this field
        template = 'lessons/create_lesson.html'
        context = {
            'form': form
        }
        return render(request, template, context)


@login_required
def edit_lesson(request, lesson_id):
    """ A view to edit and update an instructors lesson """
    profile = get_object_or_404(UserProfile, user=request.user)
    instructor_lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=instructor_lesson)
        if form.is_valid():
            form.save()
        return redirect('instructor_created_lessons')

    else:
        form = LessonForm(instance=instructor_lesson)

        if instructor_lesson.instructor_profile == profile:
            template = 'lessons/edit_lesson.html'
            context = {
                'profile': profile,
                'lesson': instructor_lesson,
                'form': form,
            }
            return render(request, template, context)
        else:
            return HttpResponse('<h1>You can only edit your own lessons, check your login details and try again<h1>', status=500)


@login_required
def review_lesson(request, lesson_id):
    """ A view to create a profile """
    profile = get_object_or_404(UserProfile, user=request.user)
    lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
    existing_review = LessonReview.objects.filter(profile=profile, lesson=lesson).first()

    template = "lessons/create_review.html"
    context = {
        'profile': profile,
        'lesson': lesson,
    }

    if request.method == 'POST':
        if not existing_review:
            form = ReviewForm(request.POST)
        else:
            form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            form.save()
            return redirect('studio', lesson.lesson_id)
        else:
            return HttpResponse('Error in review form', status=500)

    else:
        if existing_review:
            form = ReviewForm(instance=existing_review)
            context['form'] = form
            return render(request, template, context)
        else:
            form = ReviewForm(initial={'profile': profile, 'lesson': lesson})  # Insert current user in this field
            context['form'] = form
            return render(request, template, context)
