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
from cards.views import FieldView, CardTypeView

urlpatterns = [
    # Admin pages
    url(r'^admin/', admin.site.urls),
    # Main views
    url(r'^$', cardviews.home),
    url(r'^type/(?P<type_id>[0-9]+)$', cardviews.view),
    url(r'^type/(?P<type_id>[0-9]+)/layout$', cardviews.layout),
    url(r'^type/(?P<type_id>[0-9]+)/data$', cardviews.data),
    # Rest
    url(r'^field$', FieldView.as_view()),
    url(r'^field/(?P<field_id>[0-9]+)$', FieldView.as_view()),
    url(r'^cardtype/(?P<card_type_id>[0-9]+)$', CardTypeView.as_view()),
]
