from django.forms import ModelForm 
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'  # Include all fields from the Room model
          # Exclude fields that should not be set by the form