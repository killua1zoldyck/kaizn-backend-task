# kaizn_app/urls.py

from django.urls import path, re_path, reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import signup, user_login, item_dashboard, get_item_inventory
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('item_dashboard/', item_dashboard, name='item_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_item_inventory/', get_item_inventory, name='get_item_inventory'),
    re_path(r'^.*$', RedirectView.as_view(url=reverse_lazy('item_dashboard')), name='login'),
    # Add other URL patterns as needed
]
