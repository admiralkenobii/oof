from django.shortcuts import render

from .models import HotelService, Room


def home(request):
    rooms = Room.objects.all().order_by("number")
    services = HotelService.objects.all().order_by("name")

    context = {
        "rooms": rooms,
        "services": services,
    }

    return render(request, "home.html", context)