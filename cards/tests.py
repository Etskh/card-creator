from django.test import TestCase
from .models import Field, CardType, Project


class FieldTestCase(TestCase):
    def setUp(self):
        Project.objects.create(
            name='TestProject'
        )
        CardType.objects.create(
            name='TestCardType',
            project=Project.objects.get(name="TestProject")
        )
        Field.objects.create(
            name='TestField',
            style='color:#F00',
            card_type=CardType.objects.get(name="TestCardType")
        )

    def test_generates_css(self):
        """CSS generated is valid CSS"""
        title = Field.objects.get(name="TestField")
        self.assertEqual(
            title.css(),
            'width:100.0000%; top:0.0000%; text-align:left; color:#F00;'
        )

