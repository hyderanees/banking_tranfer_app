from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import BankViewSet, AccountViewSet

router = DefaultRouter()
router.register(r'bank', BankViewSet, basename='Bank')
router.register(r'account', AccountViewSet, basename='account')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
