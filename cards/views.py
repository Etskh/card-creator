from django.shortcuts import render, get_object_or_404

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
    return render(request, 'partials/field-edit.html', {
        'field': field
    })