from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

from .models import UserProfile
from checkout.models import OrderLineItem

from .forms import ProfileForm


@login_required
def profile(request):
    """ View to view the personal profile page of the logged in user """
    profile = get_object_or_404(UserProfile, user=request.user)
    profile_complete = profile.test_profile_is_complete()
    # Get purchased lessons
    Users_OrderdLineItems = OrderLineItem.objects.filter(profile=profile)

    if 'error' in request.GET:
        messages.warning(request, 'You must complete your profile first!')

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'profile_complete': profile_complete,
        'Users_OrderdLineItems': Users_OrderdLineItems,
    }
    return render(request, template, context)


@login_required
def edit_profile(request):
    """ View to edit the personal profile page of the logged in user """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        else:
            error = form.errors
            messages.error(request, f'There was an error in your profile \
                                    data: {error}, please try again.')
        return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

        context = {
            'profile': profile,
            'form': form,
        }
        return render(request, 'profiles/edit_profile.html', context)


def instructors(request):
    """ View to display list of instructors """
    valid_sort_values = ['user__username', 'rating', 'lesson_count']
    # Default sort parameters
    sort_by = 'rating'
    sort_direction = 'desc'
    current_query = ''

    # Pagination
    page_number = 1  # Default page number
    instructors_on_page = 5  # No of lessons on a page at once

    instructor_list = UserProfile.objects.filter(is_instructor=True,
                                                 lesson_count__gt=0)
    
    if request.method == 'POST':
        return redirect('instructors')

    if request.GET:
        # Get current page number if exists
        if 'page' in request.GET:
            page_number = request.GET.get('page')

        if 'sort_by' in request.GET:
            if request.GET['sort_by'] not in valid_sort_values:
                messages.error(request, 'Invalid sort value, displaying all \
                                         instructors by rating in descending \
                                         order')
                return redirect(reverse('instructors'))
            else:
                sort_by = request.GET['sort_by']

        if 'sort_direction' in request.GET:
            if request.GET['sort_direction'] != 'desc':
                sort_direction = 'asc'

        # Get Query and filter if valid
        if 'q' in request.GET:
            current_query = request.GET['q']

            instructor_list = instructor_list.filter(Q(
                user__username__icontains=current_query))
            if not instructor_list:
                messages.error(request, "Your query returned no instructors \
                                        please try again")

    # Apply Sort
    if sort_direction == 'desc':
        instructor_list = instructor_list.order_by(F(
            sort_by).desc(nulls_last=True))
    else:
        instructor_list = instructor_list.order_by(F(
            sort_by).asc(nulls_last=True))

    template = 'profiles/instructors.html'

    # Create page from Paginator
    p = Paginator(instructor_list, instructors_on_page)
    try:
        page_object = p.page(page_number)
    except EmptyPage:
        messages.error(request, "Page does not exist, returning to page 1")
        page_object = p.page(1)

    context = {
        'instructor_list': page_object,
        'sort_direction': sort_direction,
        'sort_by': sort_by,
        'current_query': current_query,
    }

    return render(request, template, context)


@login_required
def request_instructor_status(request, status):
    """ View for user to request to become an instructor """
    profile = get_object_or_404(UserProfile, user=request.user)

    profile_complete = profile.test_profile_is_complete()
    if not profile_complete:
        messages.error(request, 'Error, you must complete your profile first.')
        return redirect(reverse('profile'))

    if status == 'request':
        profile.requested_instructor_status = True
        profile.save()
    if status == 'unrequest':
        profile.requested_instructor_status = False
        profile.save()

    return redirect(reverse('profile'))
