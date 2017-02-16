from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import CardType, Field


def home(request):
    card_types = CardType.objects.all()
    return render(request, 'core/default.html', {
        'view_name': 'home',
        'card_types': card_types,
    })


def view(request, type_id):
    card_type = get_object_or_404(CardType, pk=type_id)
    card_types = CardType.objects.all()
    return render(request, 'card-list.html', {
        'view_name': 'view',
        'card_types': card_types,
        'cardtype': card_type,
        'cards': card_type.card_set.all(),
    })


def layout(request, type_id):
    card_type = get_object_or_404(CardType, pk=type_id)
    card_types = CardType.objects.all()
    return render(request, 'card-layout.html', {
        'view_name': 'layout',
        'card_types': card_types,
        'cardtype': card_type
    })


def data(request, type_id):
    card_type = get_object_or_404(CardType, pk=type_id)
    card_types = CardType.objects.all()
    cards = card_type.card_set.all()
    total_card_count = sum([card.count for card in cards])
    return render(request, 'card-data.html', {
        'view_name': 'data',
        'card_types': card_types,
        'cardtype': card_type,
        'total_card_count': total_card_count,
        'cards': card_type.card_set.all(),
    })


def field_edit(request, field_id=None):
    if request.method == 'PUT':
        card_type = get_object_or_404(CardType, name='Item')
        field = Field.objects.create(
            name='new-field',
            card_type=card_type,
        )
        return render(request, 'partials/field-span.html', {
            'field': field
        })

    field = get_object_or_404(Field, pk=field_id)
    if request.method == 'GET':
        return render(request, 'partials/field-edit.html', {
            'field': field
        })
    elif request.method == 'DELETE':
        field.delete()
        return JsonResponse({
            'success': True
        })
    elif request.method == 'POST':
        if 'top' in request.POST:
            field.height = request.POST['top']

        if 'name' in request.POST:
            field.name = request.POST['name']

        if 'template' in request.POST:
            field.template = request.POST['template']

        if 'alignment' in request.POST:
            field.alignment = request.POST['alignment']

        field.save()

        return JsonResponse({
            'success': True
        })
