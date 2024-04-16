from django.urls import path, include
from .views import (EventsViewSet, RegisterCustomEvents,
                    ListDelegatesAPIView, RetrieveUpdateDestroyDelegateAPIView,
                    EditRegisterEvents, CheckForEvents, EntertainmentViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventsViewSet)
router.register(r'events', EntertainmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register-and-add-event/', RegisterCustomEvents.as_view()),
    path('add-event-to-exist-user/', EditRegisterEvents.as_view()),
    path('delegate-list/', ListDelegatesAPIView.as_view()),
    path('qr-scan/', CheckForEvents.as_view()),
    path('delegate-list/<int:id>/', RetrieveUpdateDestroyDelegateAPIView.as_view()),
]
