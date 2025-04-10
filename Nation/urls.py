from django.urls import path

from .views import *

app_name = "nation"

urlpatterns = [
    path('', login_required(NationHomeView.as_view()), name="home"),
    path('create/', login_required(NationCreateView.as_view()), name="create"),
    path('edit_nation/images/<slug:slug>/', login_required(NationEditFormView.as_view()), name="edit_form"),
    path('edit_nation/<slug:slug>/', login_required(NationEditView.as_view()), name="edit_page"),
    path('<slug:nation_slug>/fields/', login_required(ModelFieldEndpoint.as_view()), name="edit"),
    path('<slug:slug>/', login_required(NationDetailView.as_view()), name="details"),


]
