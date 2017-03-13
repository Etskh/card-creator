from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View

from .models import Project, CardType, Field, CardTypeData, Font, Card


def home(request):
    card_types = CardType.objects.all()
    # Grab whatever card type and take the project from that
    # FIXME: security matters, kids. Just not yet
    project = card_types[0].project
    return render(request, 'core/default.html', {
        'project': project,
        'view_name': 'home',
        'card_types': card_types,
    })


def project_home(request, project_slug):

    project = Project.get_by_slug(project_slug)

    return render(request, 'core/default.html', {
        'project': project,
        'view_name': 'home',
        'card_types': project.cardtype_set.all(),
    })


def project_settings(request, project_slug):

    project = Project.get_by_slug(project_slug)

    return render(request, 'project-settings.html', {
        'project': project,
        'card_types': project.cardtype_set.all(),
    })


# TODO: Move this to its own module

class TemplateCardTypeView:
    @staticmethod
    def render(request, project_slug, card_type_slug, view_name):
        templates = {
            'view': 'card-list.html',
            'layout': 'card-layout.html',
            'data': 'card-data.html',
        }
        project = Project.get_by_slug(project_slug)

        # TODO: sanity check for card_type belonging to project
        card_type = CardType.objects.get(name=card_type_slug)
        cards = card_type.card_set.all()

        return render(request, templates[view_name], {
            'project': project,
            'card_type': card_type,
            'view_name': view_name,
            'card_types': project.cardtype_set.all(),
            'cards': card_type.card_set.all(),
            'total_card_count': sum([card.count for card in cards]),
        })






class CardView(View):

    @staticmethod
    def create(request, type_id):
        card_type = get_object_or_404(CardType, pk=type_id)

        card = Card.objects.create(
            card_type=card_type,
            title=request.POST['title'],
        )

        return render(request, 'partials/card-row.html', {
            'card_type': card_type,
            'dataset': card_type.default_dataset(),
            'card': card
        })

    def get(self, request, card_id=None):
        if not card_id:
            return render(request, 'partials/card-entry.html', {
                # empty
            })

        card = get_object_or_404(Card, pk=card_id)
        return render(request, 'partials/card-entry.html', {
            'card': card,
            'dataset': card.dataset(),
        })

    def post(self, request, card_id):
        card = get_object_or_404(Card, pk=card_id)
        card.title = request.POST['title']
        card.count = request.POST['count']

        for name, value in card.dataset():
            card.set_data(name, request.POST['data[' + name + ']'])

        for field in card.fields:
            try:
                card.set_field(field.name, request.POST['fields[' + field.name + ']'])
            except KeyError:
                pass

        card.save()

        return JsonResponse({
            'success': True
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
