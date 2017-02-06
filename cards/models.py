from django.db import models
from django.contrib.auth.admin import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField('date created')
    owner = models.ForeignKey(User, null=True, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CardType(models.Model):
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


class Field(models.Model):
    name = models.CharField(max_length=255)
    width = models.DecimalField("Width, percentage", default=1.0, max_digits=5, decimal_places=4)
    height = models.DecimalField("Distance from top, percentage", default=0.0, max_digits=5, decimal_places=4)
    alignment = models.CharField(default='left', choices=(
        ('left', 'Left'),
        ('center', 'Centre'),
        ('right', 'Right'),
    ), max_length=16)
    style = models.CharField(max_length=255,blank=True)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)

    def css(self):
        return '''
            width: {}%;
            top: {}%;
            text-align: {};
            {};
        '''.format(
            self.width * 100,
            self.height * 100,
            self.alignment,
            self.style
        )

    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(null=True, max_length=255)
    count = models.IntegerField(default=4)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)

    def __str__(self):
        print(self.fields.all())
        return self.title


class FieldData(models.Model):
    value = models.CharField(max_length=255)
    field = models.ForeignKey(Field, related_name='+', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='fields', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


