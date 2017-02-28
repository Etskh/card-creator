import json

from django.db import models
from django.contrib.auth.admin import User


class Project(models.Model):
    """
    This represents a collection of card types
    - a single board game or a prototype
    """
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField('date created', auto_now_add=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CardType(models.Model):
    """
    A single instance of a type of card
    - it has several fields and a size
    - eventually there will be a 'factory' of some sort
    - ^ it will create prototypal card types (playing card, magic card)
    """
    name = models.CharField(max_length=255)
    width = models.DecimalField(default=2.5, max_digits=3, decimal_places=2)
    height = models.DecimalField(default=4.0, max_digits=3, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    REASONABLE_MARGIN = 0.12

    def margin(self):
        return CardType.REASONABLE_MARGIN

    def inner_width(self):
        return float(self.width) - (CardType.REASONABLE_MARGIN * 2.2)

    def inner_height(self):
        return float(self.height) - (CardType.REASONABLE_MARGIN * 2.2)

    def __str__(self):
        return self.name


class CardTypeData(models.Model):
    """
    This is a single value-type associated with a card,
    such as "water-mana-cost" or "attack"
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='', blank=True)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Field(models.Model):
    """
    A single row on a card
    """
    name = models.CharField(max_length=255)
    template = models.CharField(max_length=255, blank=True, default='')
    width = models.DecimalField("Width, percentage", default=1.0, max_digits=5, decimal_places=4)
    height = models.DecimalField("Distance from top, percentage", default=0.0, max_digits=5, decimal_places=4)
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    alignment = models.CharField(default='left', choices=(
        ('left', 'Left'),
        ('center', 'Centre'),
        ('right', 'Right'),
    ), max_length=16)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)

    def css(self):
        return 'width:{}%; top:{}%; text-align:{}; font-weight:{}; font-style:{};'.format(
            self.width * 100,
            self.height * 100,
            self.alignment,
            'bold' if self.is_bold else 'normal',
            'italic' if self.is_italic else 'normal',
        )

    def __str__(self):
        return self.name


class Card(models.Model):
    """
    This is an individual card with a name and the number to put
    in a single collection
    """
    title = models.CharField(null=True, max_length=255)
    count = models.IntegerField(default=4)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    data = models.CharField(max_length=255, default='{}')

    def __str__(self):
        return self.title

    def data_value(self, name):
        values = json.loads(self.data)

        try:
            return str(values[name])
        except KeyError:
            values[name] = 0
            self.data = json.dumps(values)
            self.save()

        return values[name]

    @property
    def patterns(self):
        pattern_list = [
            ('{title}', self.title),
            ('{count}', str(self.count)),
        ]

        for data in self.card_type.cardtypedata_set.all():
            pattern_list.append(
                ('{#' + data.name + '}', self.data_value(data.name)),
            )

        print(pattern_list)

        return pattern_list

    @property
    def fields(self):
        fields = []

        for field in self.card_type.field_set.all():
            try:
                data = self.fielddata_set.get(field=field)
                field.value = data.value
            except:
                field.value = field.template
                field.inherited = True

            for pattern, replacement in self.patterns:
                field.value = field.value.replace(pattern, replacement)

            fields.append(field)

        return fields


class FieldData(models.Model):
    """
    A single field of data
    """
    value = models.CharField(max_length=255)
    field = models.ForeignKey(Field, related_name='+', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def name(self):
        return self.field.name

    def __str__(self):
        return self.value

