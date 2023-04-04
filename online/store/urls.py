"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    # path('form/', views.form_practice , name='form'),
    path('categories/', views.all_categories, name="all-categories"),
    path('<slug:categoty_slug>/', views.category_products, name="category-products"),
    path('game/<slug:game_slug>/', views.game_detail, name="game-detail"),
    path('<slug:game_slug>/comment/', views.CommentCreateView.as_view(), name='comment-add'),
    path('comment/<int:pk>/update', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

]

