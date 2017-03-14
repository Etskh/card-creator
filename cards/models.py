import json

from django.core.exceptions import ObjectDoesNotExist
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

    # TODO: Move this function to some core library
    @staticmethod
    def to_slug(string):
        """
        Creates a slug from any string
        :param string: input
        :return: {string} of slug
        """
        return string.replace(' ', '-').lower()

    @property
    def slug(self):
        """
        :return: slug of the project
        """
        return Project.to_slug(self.name)

    @staticmethod
    def get_by_slug(project_slug):
        """
        Gets the project by the slug
        :param project_slug: slug for the project
        :return: Project of slug
        :raises: ValueError if no project found
        """

        # TODO: Optimise this function
        projects = [p for p in Project.objects.all() if p.slug == project_slug]

        if len(projects) != 1:
            raise ValueError(
                '{} projects matched the slug `{}` and this is '
                'a problem, but I haven\'t gotten around to coding '
                'a graceful way to handle it.'.format(
                    len(projects),
                    project_slug,
                ))

        return projects[0]

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

    @property
    def editable_fields(self):
        """
        Gives the list of fields without a value for a default template
        :return: list of fields
        """
        fields = []
        for field in self.field_set.all():
            if len(field.template) == 0:
                fields.append(field)

        return fields

    def default_dataset(self):
        """
        Gives a list of tuples of datanames, and default values
        :return: array of tuples in the form (name, value)
        """
        return [(data.name, 0) for data in self.cardtypedata_set.all()]

    def margin(self):
        """
        Gives the margin for cards
        """
        # TODO: Could remove this function, probably
        return CardType.REASONABLE_MARGIN

    def inner_width(self):
        """
        Gets the inner-width of the card (width, minus margin) in inches
        :return: real number in inches
        """
        return float(self.width) - (CardType.REASONABLE_MARGIN * 2.2)

    def inner_height(self):
        """
        Gets the inner-height of the card (height, minus margin) in inches
        :return: real number in inches
        """
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


class Font(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='sans-serif', choices=(
        ('sans-serif', 'Sans-serif'),
        ('serif', 'Serif'),
        ('cursive', 'Cursive'),
    ))

    def css(self):
        """
        Returns the CSS for the `font-family` property
        :return: CSS string
        """
        # TODO: is this... viewey?
        return '\'{}\', {}'.format(
            self.name,
            self.type
        )

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
    font = models.ForeignKey(Font, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    font_size = models.DecimalField("Font-size, percentage", default=100, max_digits=3, decimal_places=0)
    alignment = models.CharField(default='left', choices=(
        ('left', 'Left'),
        ('center', 'Centre'),
        ('right', 'Right'),
    ), max_length=16)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)

    def css(self):
        """
        Gets the CSS for this field, if no selected font, then uses Arial
        :return: CSS string
        """
        # TODO: is this also too viewey?
        if not self.font:
            font = Font.objects.get(name='Arial')
        else:
            font = self.font

        return 'width:{}%; top:{}%; text-align:{}; font-weight:{}; ' \
               'font-style:{}; font-family:{}; font-size:{}%;'.format(
                    self.width * 100,
                    self.height * 100,
                    self.alignment,
                    'bold' if self.is_bold else 'normal',
                    'italic' if self.is_italic else 'normal',
                    font.css(),
                    self.font_size,
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

    def set_data(self, name, value):
        """
        Sets the data for a specific data name
        :param name: name of card-data
        :param value: to set for card-data
        :return: nothing
        """
        values = json.loads(self.data)
        values[name] = value
        self.data = json.dumps(values)

    def data_value(self, name):
        """
        Gets the data-value for a given card-data name, side-effect: if there is no value for that
        data in the card yet, it will default to 0 and save that in the card
        :param name: of the data
        :return: number, default 0
        """
        values = json.loads(self.data)

        try:
            return str(values[name])
        except KeyError:
            values[name] = 0
            self.data = json.dumps(values)
            self.save()

        return values[name]

    def dataset(self):
        """
        Gets the full data set of the card in the form of [( name, value),(name, value)...]
        :return: array of tuples in the form (name, value)
        """
        return [(data.name, self.data_value(data.name)) for data in self.card_type.cardtypedata_set.all()]

    def set_field(self, name, value):
        """
        Sets the value of a field. Side effect: if no field data exists for that field, then
        it will create a new field data entry
        :param name: of field
        :param value: string of new field value
        :return: nothing
        """
        field = Field.objects.get(name=name)
        try:
            field_data = self.fielddata_set.get(field=field)
            field_data.value = value
            field_data.save()
        except ObjectDoesNotExist:
            #
            # No existing data? Make a new one
            FieldData.objects.create(
                card=self,
                value=value,
                field=field,
            )

    @property
    def patterns(self):
        """
        Gets the list of patterns for this card
        :return: array of tuples in the form (pattern, replacement)
        """
        # TODO: this might need to get more complicated
        # like using regex for the pattern and a lambda function for the replacement
        pattern_list = [
            ('{title}', self.title),
            ('{count}', str(self.count)),
        ]

        for data in self.card_type.cardtypedata_set.all():
            pattern_list.append(
                ('{#' + data.name + '}', self.data_value(data.name)),
            )

        return pattern_list

    @property
    def fields(self):
        """
        Gets a list of fields, with value set to what should be displayed
        :return: an array of fields, with value
        """
        fields = []

        for field in self.card_type.field_set.all():
            try:
                data = self.fielddata_set.get(field=field)
                field.value = data.value
            except ObjectDoesNotExist:
                field.value = field.template
                field.inherited = True

            for pattern, replacement in self.patterns:
                field.value = field.value.replace(pattern, replacement)

            fields.append(field)

        return fields

    @property
    def editable_fields(self):
        """
        Like the fields property, but only gets fields without a default template
        :return: array of fields, with value (default: None)
        """
        fields = []
        for field in self.card_type.editable_fields:
            try:
                data = self.fielddata_set.get(field=field)
                field.value = data.value
            except ObjectDoesNotExist:
                field.value = None
            fields.append(field)

        return fields


class FieldData(models.Model):
    """
    A single field of data
    """
    value = models.CharField(max_length=255)
    field = models.ForeignKey(Field, related_name='+', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    @property
    def name(self):
        return self.field.name

    def __str__(self):
        return self.value

