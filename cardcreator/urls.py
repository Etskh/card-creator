"""cardcreator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cards import views as cardviews
from cards.views import FieldView, CardTypeView, CardDataView, CardView

urlpatterns = [
    # Admin pages
    url(r'^admin/', admin.site.urls),
    # Main views
    url(r'^$', cardviews.home),
    # project home
    url(r'^(?P<project_slug>[a-zA-Z\-]+)$', cardviews.project_home),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)$',
        cardviews.TemplateCardTypeView.render, {
            'view_name': 'view'
        }),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/layout$',
        cardviews.TemplateCardTypeView.render, {
            'view_name': 'layout'
        }),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/data$',
        cardviews.TemplateCardTypeView.render, {
            'view_name': 'data'
        }),


    # RESTful interface
    url(r'^type/(?P<type_id>[0-9]+)/new-card$', CardView.create),
    # Card
    url(r'^card$', CardView.as_view()),
    url(r'^card/(?P<card_id>[0-9]+)$', CardView.as_view()),
    # Fields
    url(r'^field$', FieldView.as_view()),
    url(r'^field/(?P<field_id>[0-9]+)$', FieldView.as_view()),
    #  Card Type
    url(r'^cardtype/(?P<card_type_id>[0-9]+)$', CardTypeView.as_view()),
    url(r'^cardtype/(?P<card_type_id>[0-9]+)/create$', CardTypeView.as_view()),
    # Data
    url(r'^data$', CardDataView.as_view()),
    url(r'^data/(?P<card_data_id>[0-9]+)$', CardDataView.as_view()),
]
