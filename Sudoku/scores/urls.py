"""scores app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'scores'
urlpatterns = [
    # urls relative to the name of the app (scores)
    # so scores will be prepended to each defined url
    path('', ScoreListView.as_view(), name='scores'),
    path('create/', ScoreCreateView.as_view(), name='score-create'),
    path('<int:i_id>/', ScoreDetailView.as_view(), name='score-detail'),
    path('<int:i_id>/delete/', ScoreDeleteView.as_view(), name='score-delete'),
    path('<int:i_id>/update/', ScoreUpdateView.as_view(), name='score-update')
]
