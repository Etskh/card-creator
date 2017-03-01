from django.test import TestCase
from .models import Field, CardType, Project, Font


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
            card_type=CardType.objects.get(name="TestCardType")
        )
        Font.objects.create(
            name='Arial',
            type='sans-serif',
        )

    def test_generates_css(self):
        """CSS generated is valid CSS"""
        title = Field.objects.get(name="TestField")
        self.assertEqual(
            title.css(),
            ' '.join([
                'width:100.0000%; top:0.0000%;',
                'text-align:left; font-weight:normal; font-style:normal;',
                'font-family:\'Arial\', sans-serif; font-size:100%;',
            ])
        )

