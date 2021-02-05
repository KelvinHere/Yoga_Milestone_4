from django.shortcuts import (
    render, get_object_or_404, redirect, reverse, HttpResponse
    )
from django.db.models import Q, F
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage

from .models import UserProfile
from checkout.models import OrderLineItem
from lessons.models import (
    Lesson, Subscription, LessonReview, LessonReviewFlagged
    )

import json
from yoga.utils import get_profile_or_none
from .forms import LessonForm, ReviewForm


def lessons(request):
    """ View to return the lessons page """
    # Lesson & Profile data
    profile = get_profile_or_none(request)
    lessons = Lesson.objects.all()
    subscribed_lesson_list = []
    paid_lesson_list = []

    # Default Titles
    page_title = 'All Lessons'
    sub_title = None
    filter_title = 'All Lessons'
    filter_subtitle = ''

    # Search / Sort / Filter - Default values
    valid_sort_values = ['lesson_name',
                         'instructor_profile',
                         'rating',
                         'price']
    sortby = 'rating'
    filter_by = 'all_lessons'
    sort_direction = 'desc'
    instructor_to_display = None
    query = ''

    # Pagination
    page_number = 1  # Default page number
    lessons_on_page = 5  # No of lessons on a page at once

    # If authenticated get a list of subscribed & purchased lessons
    if request.user.is_authenticated:

        subscribed_lessons = Subscription.objects.filter(user=profile)
        for subscribed_lesson in subscribed_lessons:
            subscribed_lesson_list.append(subscribed_lesson.lesson.lesson_id)

        paid_lessons = OrderLineItem.objects.filter(profile=profile)
        for paid_lesson in paid_lessons:
            paid_lesson_list.append(paid_lesson.lesson.lesson_id)

    # Handle get requests
    if request.GET:

        # Get current page number if exists
        if 'page' in request.GET:
            page_number = request.GET.get('page')

        # Sort by - Only change default sort value if it is valid
        if 'sort' in request.GET:
            if request.GET['sort'] in valid_sort_values:
                sortby = request.GET['sort']

        # Sort Direction
        if 'direction' in request.GET:
            if request.GET['direction'] == 'asc':
                sort_direction = 'asc'
            else:
                sort_direction = 'desc'

        # Filter lessons
        if 'filter' in request.GET:
            if request.GET['filter'] == 'subscribed_lessons':
                lessons = lessons.filter(lesson_id__in=subscribed_lesson_list)
                filter_by = request.GET['filter']
                page_title = 'Subscribed Lessons'
                filter_title = 'Subscribed Lessons'
                if not lessons:
                    sub_title = 'You are currently not subscribed to any \
                                 lessons'

            if request.GET['filter'] == 'purchased_lessons':
                lessons = lessons.filter(lesson_id__in=paid_lesson_list)
                filter_by = request.GET['filter']
                page_title = 'Purchased Lessons'
                filter_title = 'Purchaed Lessons'
                if not lessons:
                    sub_title = 'You have not purchased any lessons'

        # Add instructor header to page
        if 'instructor' in request.GET:
            if request.GET['instructor']:
                instructor_id = request.GET['instructor']
                try:
                    instructor_to_display = get_object_or_404(UserProfile,
                                                              id=instructor_id)
                    if not instructor_to_display.is_instructor:
                        messages.error(request,
                                       'This user is not an instructor, \
                                       please pick one from the list.')
                        return redirect(reverse('instructors'))
                except Exception:
                    messages.error(request,
                                   'Instructor not found, please pick \
                                    one from the instructor list.')
                    return redirect(reverse('instructors'))
                page_title = f"Welcome to {instructor_to_display}'s Studio"
                filter_subtitle = f" in {instructor_to_display}'s Studio"
                lessons = lessons.filter(
                    instructor_profile=instructor_to_display
                    )

        # Get Query and filter if valid
        if 'q' in request.GET:
            query = request.GET['q']

            lessons = lessons.filter(Q(lesson_name__icontains=query))
            if not lessons:
                messages.error(request, "Your query returned no lessons \
                                         please try again")

    # Apply Sort direction
    if sort_direction == 'asc':
        lessons = lessons.order_by(F(sortby).asc(nulls_last=True))
    else:
        lessons = lessons.order_by(F(sortby).desc(nulls_last=True))

    # Create page from Paginator
    p = Paginator(lessons, lessons_on_page)
    try:
        page_object = p.page(page_number)
    except EmptyPage:
        messages.error(request, "Page does not exist, returning to page 1")
        page_object = p.page(1)

    # Create template and context
    template = 'lessons/lessons.html'
    context = {
        # Lesson and profile data
        'profile': profile,
        'lessons': page_object,
        'subscribed_lesson_list': subscribed_lesson_list,
        'paid_lesson_list': paid_lesson_list,
        # Titles
        'page_title': page_title,
        'sub_title': sub_title,
        'filter_title': filter_title,
        'filter_subtitle': filter_subtitle,
        # Filters / Sorting / Searching
        'sort_by': sortby,
        'sort_direction': sort_direction,
        'filter_by': filter_by,
        'instructor_to_display': instructor_to_display,
        'current_query': query,
        'show_discount_banner': True,
    }

    return render(request, template, context)


@login_required
def subscriptions(request):
    """ View to remove a subscribed lesson from a UserProfile """
    if request.method == 'GET':
        profile = get_object_or_404(UserProfile, user=request.user)
        try:
            lesson_id = request.GET['lesson_id']
            lesson_object = Lesson.objects.get(lesson_id=lesson_id)
        except Exception:
            messages.error(request,
                           'Invalid request, no lessons have been subscribed \
                           or unsubscribed to.')
            return redirect(reverse('lessons'))

        if request.GET['subscribe'] == 'false':
            unsubscribe = Subscription.objects.filter(lesson=lesson_object,
                                                      user=profile)
            unsubscribe.delete()
            json_response = json.dumps({'subscription_status': 'unsubscribed'})
            return HttpResponse(json_response, content_type='application/json')

        elif request.GET['subscribe'] == 'true':
            if not Subscription.objects.filter(lesson=lesson_object,
                                               user=profile).exists():
                Subscription.objects.create(lesson=lesson_object, user=profile)
            json_response = json.dumps({'subscription_status': 'subscribed'})
            return HttpResponse(json_response, content_type='application/json')

        else:
            messages.error(request, 'Invalid request, no lessons have been \
                                    subscribed or unsubscribed to.')
            return redirect(reverse('lessons'))


@login_required
def instructor_admin(request):
    """ View admin for lessons instructors have created """

    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_instructor:
        messages.error(request, 'Only instructors can do this.')
        return redirect('home')

    template = 'lessons/instructor_admin.html'

    # Get lessons instructor created
    instructor_created_lessons = Lesson.objects.filter(
        instructor_profile=profile)
    customer_purchases = OrderLineItem.objects.filter(
        lesson__in=instructor_created_lessons).values_list('lesson', flat=True)
    sales = OrderLineItem.objects.filter(
        lesson__in=instructor_created_lessons).order_by('-order__date')

    context = {
        'profile': profile,
        'instructor_created_lessons': instructor_created_lessons,
        'customer_purchases': customer_purchases,
        'sales': sales,
    }

    return render(request, template, context)


@login_required
def delete_lesson(request, id):
    """ A view to delete a lesson given a lesson_id """
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_instructor:
        messages.error(request, 'Only instructors can do this.')
        return redirect('home')

    try:
        print('##')
        print(id)
        lesson = get_object_or_404(Lesson, lesson_id=id)
        purchased = OrderLineItem.objects.filter(lesson=lesson)
    except Exception:
        messages.error(request, 'Invalid lesson ID, no lessons were deleted.')
        return redirect(reverse('instructor_admin'))

    if purchased:
        messages.error(request, 'You cannot delete a lesson customers have \
                                purchased, you can only edit.')
        return redirect(reverse('instructor_admin'))

    if lesson.instructor_profile == profile:
        instructor_profile = lesson.instructor_profile
        lesson.delete()
        total_lessons = Lesson.objects.filter(
            instructor_profile=instructor_profile).count()
        instructor_profile._update_lesson_count(total_lessons)
        messages.success(request, 'Lesson deleted.')
        return redirect('instructor_admin')
    else:
        messages.error(request, 'This lesson does not belong to you and has \
                                not been deleted, please check your username \
                                and try again.')
        return redirect(reverse('instructor_admin'))


@login_required
def create_lesson(request):
    """ View to create an instructor lesson """
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_instructor:
        messages.error(request, 'Only instructors can do this.')
        return redirect('home')

    if request.method == 'POST':
        # Get lesson name form data
        lesson_name = request.POST.get('lesson_name')

        # Check for duplicate names
        instructor_created_lessons = Lesson.objects.filter(
            instructor_profile=profile).values_list('lesson_name', flat=True)

        if lesson_name not in instructor_created_lessons:
            # Create lesson
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.instructor_profile = profile
                lesson.save()
                return redirect('instructor_admin')
            return redirect('instructor_admin')
        else:
            messages.error(request, 'You already have a lesson named this.')
            return redirect(reverse('instructor_admin'))

    else:
        form = LessonForm(initial={'instructor_profile': profile})
        template = 'lessons/create_lesson.html'
        context = {
            'form': form
        }
        return render(request, template, context)


@login_required
def edit_lesson(request, lesson_id):
    """ A view to edit and update an instructors lesson """
    profile = get_object_or_404(UserProfile, user=request.user)
    if not profile.is_instructor:
        messages.error(request, 'Only instructors can do this.')
        return redirect('home')

    try:
        instructor_lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
    except Exception:
        messages.error(request, 'Invalid lesson ID, no lessons were updated.')
        return redirect(reverse('instructor_admin'))

    if request.method == 'POST':
        form = LessonForm(request.POST,
                          request.FILES,
                          instance=instructor_lesson)
        if form.is_valid():
            form.save()
        return redirect('instructor_admin')

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
            messages.error(request, 'You can only edit your own lessons, \
                                     please check your username.')
            return redirect(reverse('instructor_admin'))


@login_required
def review_lesson(request, lesson_id):
    """ A view to create a profile """
    profile = get_object_or_404(UserProfile, user=request.user)
    # Make sure lesson is valid
    try:
        lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
    except Exception:
        messages.error(request, 'Cannot create/edit a review for \
                                 an invalid lesson.')
        return redirect(reverse('home'))

    existing_review = LessonReview.objects.filter(profile=profile,
                                                  lesson=lesson).first()
    # Check existing review belongs to current users profile
    if existing_review:
        if not existing_review.profile == profile:
            messages.error(request, 'Cannot complete request, this \
                                     review is not yours.')
            return redirect(reverse('home'))

    template = "lessons/create_review.html"
    context = {
        'profile': profile,
        'lesson': lesson,
    }

    # Submit review form
    if request.method == 'POST':
        post_data = request.POST.copy()
        # Validate rating
        rating_value = request.POST['rating_dropdown']
        if int(rating_value) not in range(1, 11):
            messages.error(request, 'You entered an invalid rating, \
                                     please try again.')
            return redirect('studio', lesson.lesson_id)
        else:
            rating_value = int(rating_value)
            post_data.update({'rating': rating_value})

        # Create or fetch existing review
        if not existing_review:
            form = ReviewForm(post_data)
        else:
            form = ReviewForm(post_data, instance=existing_review)
        # Update form or return error message
        if form.is_valid():
            review = form.save(commit=False)
            review.rating = rating_value
            review.save()
            return redirect('studio', lesson.lesson_id)
        else:
            error = form.errors
            messages.error(request, f'Error in review form: {error}')
            return redirect('studio', lesson.lesson_id)
    # Send user to create/update review form
    else:
        if existing_review:
            form = ReviewForm(instance=existing_review)
            form.fields["rating_dropdown"].initial = existing_review.rating
            context['form'] = form
            return render(request, template, context)
        else:
            form = ReviewForm(initial={'profile': profile, 'lesson': lesson})
            context['form'] = form
            return render(request, template, context)


@login_required
def delete_review(request, review_pk):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Get review
    try:
        review = get_object_or_404(LessonReview, pk=review_pk)
        lesson = review.lesson
    except Exception:
        messages.error(request, 'Cannot delete review, review not found.')
        return redirect(reverse('home'))

    if review.profile == profile or request.user.is_superuser:
        review.delete()
        lesson._update_rating()
        if request.user.is_superuser and request.method == 'POST':
            # Stay on superuser admin page
            json_response = json.dumps({'success': 'True'})
            return HttpResponse(json_response, content_type='application/json')
        else:
            # Reload lesson page
            messages.success(request, 'Review deleted.')
            return redirect(reverse('studio', args=(lesson.lesson_id,)))
    else:
        messages.error(request, 'Cannot delete review, it does not belong \
                                 to this account.')
        return redirect(reverse('studio', args=(lesson.lesson_id,)))


@login_required
def flag_review(request, review_pk, lesson_id):
    """ Allows user to flag a review to admin """
    profile = get_object_or_404(UserProfile, user=request.user)

    try:
        review = get_object_or_404(LessonReview, pk=review_pk)
    except Exception:
        messages.error(request, "Invalid review, please contact support if \
                                 you think this is an error")
        return redirect(reverse('studio', args=(lesson_id,)))

    if LessonReviewFlagged.objects.filter(
            profile=profile, review=review).exists():
        messages.error(request, f"You have already flagged {review.profile}'s \
                                  review, it will be reviewd by an \
                                  administrator soon")
        return redirect(reverse('studio', args=(review.lesson.lesson_id,)))

    flag = LessonReviewFlagged(profile=profile, review=review)
    flag.save()
    messages.success(request, f"{review.profile}'s review has been flagged \
                                and will be reviewed by an administrator soon")
    return redirect(reverse('studio', args=(review.lesson.lesson_id,)))


@login_required
def remove_flag(request, flagged_review_pk):
    """ Removes all flags from a review """
    if not request.user.is_superuser:
        messages.error('Only administrators can perform this action.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        try:
            flagged_review_pk = request.POST['flagged_review_pk']
            review_to_ignore = get_object_or_404(LessonReview,
                                                 pk=flagged_review_pk
                                                 )
        except Exception:
            json_response = json.dumps({'removed_flag': 'False'})
            return HttpResponse(json_response, content_type='application/json')

        # Remove all flags for this review
        LessonReviewFlagged.objects.filter(review=review_to_ignore).delete()
        json_response = json.dumps({'removed_flag': 'True'})
        return HttpResponse(json_response, content_type='application/json')

    else:
        messages.error(request, "Remove flag does not accept GET requests")
        return redirect(reverse('superuser_admin'))


def get_modal_data(request):
    """ Get data for lesson extra detail modal """
    if request.method == 'POST':
        if 'lesson_id' in request.POST:
            lesson_id = request.POST['lesson_id']
            # Get lesson, pass it to lesson_modal template and turn to string
            if not Lesson.objects.filter(lesson_id=lesson_id).exists():
                json_response = json.dumps({'status': 'invalid_lesson'})
                return HttpResponse(json_response,
                                    content_type='application/json'
                                    )

            # Get lesson and its reviews
            lesson = Lesson.objects.get(lesson_id=lesson_id)
            lesson_reviews = LessonReview.objects.filter(
                lesson=lesson).order_by('-date')

            review_count = lesson_reviews.count()
            MEDIA_URL_for_json = settings.MEDIA_URL
            modal_string = render_to_string(
                'lessons/includes/lesson_modal.html',
                {
                    'lesson': lesson,
                    'lesson_reviews': lesson_reviews,
                    'review_count': review_count,
                    'MEDIA_URL_for_json': MEDIA_URL_for_json
                }
            )

            json_response = json.dumps({'status': 'valid_lesson',
                                        'modal': modal_string,
                                        })
            return HttpResponse(json_response, content_type='application/json')
        else:
            json_response = json.dumps({'status': 'invalid_request'})
            return HttpResponse(json_response, content_type='application/json')
    else:
        messages.error(request, 'You cannot perform this action')
        return redirect(reverse('home'))
