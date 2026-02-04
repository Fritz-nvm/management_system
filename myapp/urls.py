from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("branches/", views.branch_list, name="branch_list"),
    path("branches/add/", views.branch_add, name="branch_add"),
    path("branches/<int:branch_id>/edit/", views.branch_edit, name="branch_edit"),
    path("assets/", views.asset_list, name="asset_list"),
    path("assets/add/", views.asset_add, name="asset_add"),
    path("assets/<int:asset_id>/", views.asset_detail, name="asset_detail"),
    path("assets/<int:asset_id>/edit/", views.asset_edit, name="asset_edit"),
    path("assets/<int:asset_id>/delete/", views.asset_delete, name="asset_delete"),
]
