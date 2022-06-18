from django.contrib import admin
from django.urls import path, include
from .views import ListFortunePoolsView, FortuneEntryView, FortuneImageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('media/<str:media_key>.jpg/', FortuneImageView.as_view(), name="media-display"),

    path('api/', ListFortunePoolsView.as_view()),
    path("api/pool/<str:pool_name>/", FortuneEntryView.as_view()),

    path('api/admin/', include("fortune_admin.urls"))
]
