"""sudoku URL Configuration

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
from django.urls import include, path
from solver.views import home_view, HomeView

urlpatterns = [
    path('scores/', include('scores.urls')),
    path('admin/', admin.site.urls),
    #path('', home_view, name='home')
    path('', HomeView.as_view(), name='home')

    # DEFINED in scores/urls.py and included with scores.urls
    #
    #path('scores/', scores_view, name='scores'),
    #path('scores/create/', score_create_view, name='score-create'),
    #path('scores/<int:i_id>/delete/', score_delete_view, name='score-delete'),
    #path('scores/<int:i_id>/update/', score_update_view, name='score-update'),
    #path('scores/<int:i_id>/', dynamic_lookup_view, name='score-detail')
]
