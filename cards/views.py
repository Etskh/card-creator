from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import CardType, Field


def home(request):
    cardtype = get_object_or_404(CardType, name='Item')
    return render(request, 'card-list.html', {
        'cardtype': cardtype,
        'cards': cardtype.card_set.all(),
    })


def edit(request):
    cardtype = get_object_or_404(CardType, name='Item')
    return render(request, 'card-edit.html', {
        'cardtype': cardtype
    })


def field_edit(request, field_id):
    field = get_object_or_404(Field, pk=field_id)

    if request.method == 'GET':
        return render(request, 'partials/field-edit.html', {
            'field': field
        })

    elif request.method == 'POST':
        if 'top' in request.POST:
            field.height = request.POST['top']

        if 'name' in request.POST:
            field.name = request.POST['name']

        if 'alignment' in request.POST:
            field.alignment = request.POST['alignment']

        field.save()

        return JsonResponse({
            'success': True
        })
