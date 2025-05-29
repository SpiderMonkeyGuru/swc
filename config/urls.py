from django.urls import include, path

from api.views import expand_url

urlpatterns = [
    path("api/", include("api.urls")),
    path("<str:short_code>/", expand_url, name="expand_url"),
]
