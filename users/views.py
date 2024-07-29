from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .forms import UserRegisterForm, PaintingForm, UserUpdateForm, ProfileUpdateForm, MessageForm
from .models import Painting, Profile, Notification, Message
from django.http import JsonResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('users:welcome')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:welcome')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:home')


@login_required
def welcome(request):
    return render(request, 'users/welcome.html', {'username': request.user.username})


@login_required
def upload_painting(request):
    if request.method == 'POST':
        form = PaintingForm(request.POST, request.FILES)
        if form.is_valid():
            painting = form.save(commit=False)
            painting.user = request.user
            painting.save()
            return redirect('users:my_paintings')
    else:
        form = PaintingForm()
    return render(request, 'users/upload_painting.html', {'form': form})



# class UserProfileView(View):
#     def get(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         return render(request, 'users/profile.html', {'profile_user': user})


@login_required
def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    if not hasattr(profile_user, 'profile'):
        Profile.objects.create(user=profile_user)

    if request.method == "POST":
        if request.user != profile_user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")

        u_form = UserUpdateForm(request.POST, instance=profile_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('users:profile', pk=profile_user.pk)
    else:
        u_form = UserUpdateForm(instance=profile_user)
        p_form = ProfileUpdateForm(instance=profile_user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile_user': profile_user
    }

    return render(request, 'users/profile.html', context)


@login_required
def inbox(request):
    user_chats = Message.objects.filter(recipient=request.user).values('sender').distinct()
    chat_messages = {}
    for chat in user_chats:
        sender_id = chat['sender']
        sender = User.objects.get(id=sender_id)
        messages = Message.objects.filter(sender=sender, recipient=request.user)
        chat_messages[sender] = messages

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            recipient = User.objects.get(username=request.POST.get('recipient_username'))
            message.recipient = recipient
            message.save()
            Notification.objects.create(user=message.recipient, message=f'New message from {message.sender.username}')
            return JsonResponse({'status': 'success', 'message': message.content, 'sender': message.sender.username})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = MessageForm()
    return render(request, 'users/inbox.html', {'chat_messages': chat_messages, 'form': form})



@login_required
def send_message(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            Notification.objects.create(user=message.recipient, message=f'New message from {message.sender.username}')
            return redirect('users:inbox')
    else:
        form = MessageForm()
    return render(request, 'users/send_message.html', {'form': form, 'recipient_username': recipient_username})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'users/notifications.html', {'notifications': notifications})



















