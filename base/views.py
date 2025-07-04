from django.shortcuts import render
from .models import Room
# rooms = [
#     { 'id': 1, 'name': 'Let"s learn python'},
#     { 'id': 2, 'name': 'Design with Figma'},
#     { 'id': 3, 'name': 'Frontend development with React' },
# ]



def home(request):
    rooms = Room.objects.all()  # Fetch all rooms from the database
    context = {
        'rooms': rooms,
    }
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)  # Fetch the room by primary key
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context)

