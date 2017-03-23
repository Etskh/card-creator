from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.views import View

from .models import Project, CardType, Field, CardTypeData, Font, Card
from .apps import CardsConfig


class TemplateView:

    def __init__(self, request, view_name):
        templates = {
            'project': 'project-settings.html',
            'view': 'card-list.html',
            'layout': 'card-layout.html',
            'data': 'card-data.html',
            # These are called via AJAX only
            'ajax-card-popup': 'partials/card-entry.html',
            'ajax-card-row': 'partials/card-row.html',
            'ajax-field-span': 'partials/field-span.html',
            'ajax-field-edit': 'partials/field-edit.html',
        }
        # TODO: Make sure if the view-name is 'ajax-*' then request is AJAX

        self.request = request
        self.view_name = view_name
        self.template = templates[view_name]
        self.context = {
            'view_name': self.view_name,
            'version': CardsConfig.version_full,
        }

    def add_project(self, project_slug):
        project = Project.get_by_slug(project_slug)
        self.context['project'] = project
        self.context['card_types'] = project.cardtype_set.all()

    def add_card_type(self, card_type_slug):
        card_type = CardType.objects.get(name=card_type_slug)
        cards = card_type.card_set.all()
        self.context['card_type'] = card_type
        self.context['cards'] = card_type.card_set.all()
        self.context['total_card_count'] = sum([card.count for card in cards])

    def render(self):
        return render(self.request, self.template, self.context)


class RestView(View):

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        for field in self.fields:
            if field in request.POST:
                setattr(obj, field, request.POST[field])

        if hasattr(self, 'before_save'):
            self.before_save()

        obj.save()

        return JsonResponse({
            'success': True,
            'id': obj.id,
        })

    def put(self, request):

        if not hasattr(self, 'create_object'):
            raise Http404("Method doesn't exist.")

        obj = self.create_object(request)
        obj.save()

        return JsonResponse({
            'success': True,
            'id': obj.id,
        })

    def delete(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({
            'success': True,
        })











def home(request):
    return redirect('/trekcthulu')


def project(request, project_slug):
    view = TemplateView(request, 'project')
    view.add_project(project_slug)
    return view.render()


def card_type(request, project_slug, card_type_slug, view_name):
    view = TemplateView(request, view_name)
    view.add_project(project_slug)
    view.add_card_type(card_type_slug)
    # TODO: Sanity check that card_type's owner is project
    return view.render()






def ajax_card_popup(request, project_slug, card_type_slug, card_id):
    card = get_object_or_404(Card, pk=card_id)

    view = TemplateView(request, 'ajax-card-popup')
    view.add_project(project_slug)
    view.add_card_type(card_type_slug)
    view.context['card'] = card
    view.context['dataset'] = card.dataset()

    return view.render()


def ajax_new_card_popup(request, project_slug, card_type_slug):

    view = TemplateView(request, 'ajax-card-popup')
    view.add_project(project_slug)
    view.add_card_type(card_type_slug)

    return view.render()


def ajax_card_row(request, project_slug, card_type_slug, card_id):
    card = get_object_or_404(Card, pk=card_id)

    view = TemplateView(request, 'ajax-card-row')
    view.add_project(project_slug)
    view.add_card_type(card_type_slug)
    view.context['card'] = card
    view.context['dataset'] = view.context['card_type'].default_dataset()

    return view.render()


def ajax_field_edit(request, project_slug, card_type_slug, field_id):
    field = get_object_or_404(Field, pk=field_id)

    view = TemplateView(request, 'ajax-field-edit')
    view.context['field'] = field
    view.context['fonts'] = Font.objects.all()

    return view.render()


def ajax_field_span(request, project_slug, card_type_slug, field_id):
    field = get_object_or_404(Field, pk=field_id)

    view = TemplateView(request, 'ajax-field-span')
    view.context['field'] = field

    return view.render()















class CardRestView(RestView):
    model = Card
    fields = ['title', 'count']

    def before_save(self, request, card):
        for name, value in card.dataset():
            card.set_data(name, request.POST['data[' + name + ']'])

        for field in card.fields:
            try:
                card.set_field(field.name, request.POST['fields[' + field.name + ']'])
            except KeyError:
                pass

    def create_object(self, request):
        card_type = get_object_or_404(CardType, pk=request.POST['card_type_id'])
        return Card.objects.create(
            card_type=card_type,
            title=request.POST['title'],
        )


class CardTypeRestView(RestView):
    model = CardType
    fields = ['name']


class FieldRestView(RestView):
    model = Field
    fields = [
        'name',
        'top',
        'template',
        'alignment',
        'font_size',
    ]

    def before_save(self, request, obj):
        if 'is_bold' in request.POST:
            obj.is_bold = request.POST['is_bold'] == 'true'
        if 'is_italic' in request.POST:
            obj.is_italic = request.POST['is_italic'] == 'true'
        if 'font_id' in request.POST:
            font = get_object_or_404(Font, pk=request.POST['font_id'])
            obj.font = font

    def create_object(self, request):
        # TODO: Make this work
        card_type = get_object_or_404(CardType, name='Items')
        return Field.objects.create(
            name='new-field',
            card_type=card_type,
        )


class CardDataRestView(RestView):
    model = CardTypeData
    fields = ['name']

    def create_object(self):
        card_type = get_object_or_404(CardType, name='Items')
        return CardTypeData.objects.create(
            name='new-data-type',
            card_type=card_type,
        )

