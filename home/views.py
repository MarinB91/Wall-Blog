from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Message, CastedVotes
from .forms import MessageForm


def messages(request):
    # Fetching ten latest messages
    home_page_messages = Message.objects.order_by('-time')

    # Homepage form for creating new messages
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.username = request.user
            form_data.save()
            return redirect('messages')

    # Deleting last message if total message count exceeds 6
    if Message.objects.count() > 6:
        last_message = home_page_messages.last()
        Message.objects.get(title=last_message).delete()

    context = {
        'home_page_messages': home_page_messages,
        'form': form,
    }
    return render(request, 'home.html', context)


def top_message(request):
    from django.db.models import Count
    # Searching for most upvoted Message in CastedVotes table
    query = Message.objects.filter(castedvotes__vote='upvote').annotate(num=Count('title')).order_by('-num')[:5]
    msg = query[0]
    top_rtd_msg = Message.objects.get(title=str(msg))

    context = {
        'most_popular_msg': top_rtd_msg
    }
    return render(request, 'top_message.html', context)


def delete(request, title):
    message_to_delete = Message.objects.get(title=title)
    message_to_delete.delete()
    return redirect('messages')


def individual_message(request, title):
    single_message = Message.objects.get(title=title)
    usr = request.user
    context = {
        'single_message': single_message,
        'user': usr
    }
    return render(request, 'individual_message.html', context)


def login_page(request):
    type = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('messages')
    context = {
        'type': type
    }
    return render(request, 'registration_login.html', context)


def logout_user(request):
    logout(request)
    return redirect('messages')


def register_user(request):
    type = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messages')

    context = {'type': type,
               'form': form
               }
    return render(request, 'registration_login.html', context)


@login_required(login_url='registration_login')
def vote(request, name):
    # Fetching User and Message instances
    user = request.user
    message = Message.objects.get(title=name)

    # Creating identifier
    str_usr = str(user)
    str_mes = str(message)
    str_id = str_usr + '_' + str_mes

    cst_vts = CastedVotes.objects.filter(identification=str_id)
    if not cst_vts.exists():

        new_vote_record = CastedVotes()  # Creating new CastedVotes record
        new_vote_record.save()

        new_vote_record.username.add(user)
        new_vote_record.message.add(message)

        new_vote_record.identification = str_id
        new_vote_record.save()

        url_path = request.path  # Fetching request URL
        url_name = str(name)
        url_upvote = '/upvote/' + url_name  # Stitching expected URL for comparison

        if url_path == url_upvote:
            new_vote_record.vote = 'upvote'
            new_vote_record.save()

        else:
            new_vote_record.vote = 'downvote'
            new_vote_record.save()

        return redirect('messages')

    else:
        return redirect('messages')
