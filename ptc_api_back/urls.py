from django.conf.urls import url, include
from django.contrib import admin
from ptc_api_back import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'trips', views.TripViewSet)
router.register(r'segments', views.SegmentViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'countries', views.CountryListViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]