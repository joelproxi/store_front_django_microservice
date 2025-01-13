
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from order.views import OrderViewset


router = DefaultRouter()
router.register('orders', OrderViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
