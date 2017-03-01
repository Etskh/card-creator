from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View

from .models import CardType, Field, CardTypeData, Font


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


class CardTypeView(View):

    def post(self, request, card_type_id):
        card_type = get_object_or_404(CardType, pk=card_type_id)
        card_type.name = request.POST['name']

        card_type.save()

        return JsonResponse({
            'success': True
        })


class CardDataView(View):

    def put(self, request):
        card_type = get_object_or_404(CardType, name='Items')
        card_data = CardTypeData.objects.create(
            name='new-data-type',
            card_type=card_type,
        )
        return render(request, 'partials/data-edit.html', {
            'data': card_data
        })

    def post(self, request, card_data_id):
        card_data = get_object_or_404(CardTypeData, pk=card_data_id)
        card_data.name = request.POST['name']

        card_data.save()

        return JsonResponse({
            'success': True
        })


class FieldView(View):

    def get(self, request, field_id):
        field = get_object_or_404(Field, pk=field_id)
        return render(request, 'partials/field-edit.html', {
            'field': field,
            'fonts': Font.objects.all(),
        })

    def post(self, request, field_id):
        field = get_object_or_404(Field, pk=field_id)
        if 'top' in request.POST:
            field.height = request.POST['top']

        if 'name' in request.POST:
            field.name = request.POST['name']

        if 'is_bold' in request.POST:
            field.is_bold = request.POST['is_bold'] == 'true'

        if 'is_italic' in request.POST:
            field.is_italic = request.POST['is_italic'] == 'true'

        if 'template' in request.POST:
            field.template = request.POST['template']

        if 'alignment' in request.POST:
            field.alignment = request.POST['alignment']

        if 'font_id' in request.POST:
            font = get_object_or_404(Font, pk=request.POST['font_id'])
            field.font = font

        if 'font_size' in request.POST:
            field.font_size = request.POST['font_size']

        field.save()

        return JsonResponse({
            'success': True
        })

    def delete(self, request, field_id):
        field = get_object_or_404(Field, pk=field_id)
        field.delete()
        return JsonResponse({
            'success': True
        })

    def put(self, request):
        card_type = get_object_or_404(CardType, name='Items')
        field = Field.objects.create(
            name='new-field',
            card_type=card_type,
        )
        return render(request, 'partials/field-span.html', {
            'field': field
        })
