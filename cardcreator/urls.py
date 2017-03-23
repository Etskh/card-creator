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
from cards.views import FieldRestView, CardTypeRestView, CardDataRestView, CardRestView


"""

  Templates

    /:project                           -> Template.project
    /:project/settings                  -> ||
    /:project/:card_type                -> Template.card_type
    /:project/:card_type/layout         -> ||
    /:project/:card_type/edit           -> ||
    /:project/:card_type/new           -> Template.new_card
    /:project/:card_type/:card_id/edit -> Template.card_edit

  REST

    /card/:id
    /card/:id
    /card/:id

"""


urlpatterns = [
    # Admin pages
    url(r'^admin/', admin.site.urls),

    # Main views
    url(r'^$', cardviews.home),

    # TODO: refactor everything with project_slug to its own url file
    #
    # Project
    url(r'^(?P<project_slug>[a-zA-Z\-]+)$',
        cardviews.project),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/settings$',
        cardviews.project),
    #
    # Card Type
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)$',
        cardviews.card_type, {'view_name': 'view'}),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/layout$',
        cardviews.card_type, {'view_name': 'layout'}),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/data$',
        cardviews.card_type, {'view_name': 'data'}),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/layout$',
        cardviews.card_type, {'view_name': 'layout'}),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/data$',
        cardviews.card_type, {'view_name': 'data'}),

    #
    # Cards
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/new-card$', cardviews.ajax_new_card_popup),
    url(r'^(?P<project_slug>[a-zA-Z\-]+)/(?P<card_type_slug>[a-zA-Z\-]+)/(?P<card_id>[0-9]+)/edit$',
        cardviews.ajax_card_popup),


    # RESTful interface
    # TODO: move this away
    # Card
    url(r'^api/card$', CardRestView.as_view()),
    url(r'^api/card/(?P<pk>[0-9]+)$', CardRestView.as_view()),
    # Fields
    url(r'^api/field$', FieldRestView.as_view()),
    url(r'^api/field/(?P<pk>[0-9]+)$', FieldRestView.as_view()),
    #  Card Type
    url(r'^api/cardtype$', CardTypeRestView.as_view()),
    url(r'^api/cardtype/(?P<pk>[0-9]+)$', CardTypeRestView.as_view()),
    # Data
    url(r'^api/data$', CardDataRestView.as_view()),
    url(r'^api/data/(?P<pk>[0-9]+)$', CardDataRestView.as_view()),
]
