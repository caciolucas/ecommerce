from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewSet
from commerce.views import ProductViewSet, CartViewSet, OrderViewSet

app_name = "commerce"

router = DefaultRouter()

router.register("products", ProductViewSet, basename="products")
router.register("carts", CartViewSet, basename="carts")
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
