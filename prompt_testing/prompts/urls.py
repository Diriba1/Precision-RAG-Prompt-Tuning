from django.urls import path
from . import views

urlpatterns = [
    path('prompts/', views.prompt_list, name='prompt_list'),
    path('prompts/create/', views.prompt_create, name='prompt_create'),
    path('prompts/<int:pk>/matchup/', views.prompt_matchup, name='prompt_matchup'),
    path('', views.home_view, name='home'),
    path('generate_prompt/', views.generate_prompt_view, name='generate_prompt'),
    # ... other URLs
]
