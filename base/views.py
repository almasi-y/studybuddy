from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     { 'id': 1, 'name': 'Let"s learn python'},
#     { 'id': 2, 'name': 'Design with Figma'},
#     { 'id': 3, 'name': 'Frontend development with React' },
# ]

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, "Username or password is incorrect")

    context = {
        
    }
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )

    topics = Topic.objects.all()  # Fetch all topics from the database
    rooms_count = rooms.count()  # Get the count of rooms
    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
    }
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)  # Fetch the room by primary key
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='login')  # Ensure user is logged in to create a room
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()  # Save the room to the database
            return redirect('home')  # Redirect to home after saving
        
    context = {
        'form': form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  # Ensure user is logged in to update a room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)  # Fetch the room by primary key
    form = RoomForm(instance=room)  # Create a form instance with the room data
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()  # Save the updated room to the database
            return redirect('home')  # Redirect to home after updating
    
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  # Ensure user is logged in to delete a room
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)  # Fetch the room by primary key
    if request.method == 'POST':
        room.delete()  # Delete the room from the database
        return redirect('home')  # Redirect to home after deletion
    return render(request, 'base/delete.html', {'obj': room})
