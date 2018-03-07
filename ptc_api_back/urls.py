from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

from ptc_api_back import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'segments', views.SegmentViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'countries', views.CountryListViewSet)
router.register(r'airports', views.AirportListViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]

