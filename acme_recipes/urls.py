from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from acme_recipes.views import JWTAuthGraphQLView
from acme_recipes.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('graphql/', JWTAuthGraphQLView.as_view(schema=schema)),
]
