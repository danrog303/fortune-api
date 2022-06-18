from django.urls import path
from fortune_admin.views import ApplicableTriggerView, ImageListCreateView, PoolListCreateView, EntryListCreateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('applicable-trigger/', ApplicableTriggerView.as_view()),
    path('image/', ImageListCreateView.as_view()),
    path("pool/", PoolListCreateView.as_view()),
    path("entry/", EntryListCreateView.as_view()),
    path("auth/", obtain_auth_token)
]
