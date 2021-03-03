from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .jwt import RichTokenObtainPairView

api_info = openapi.Info(
    title="Recnik API",
    default_version='v1',
    description="Recnik API Description",
    terms_of_service="https://rsj.rs/",
    contact=openapi.Contact(email="mbranko@uns.ac.rs"),
    license=openapi.License(name="GPL v3 License"),
)

schema_view = get_schema_view(
   openapi.Info(
      title="Recnik API",
      default_version='v1',
      description="Recnik API Description",
      terms_of_service="https://rsj.rs/",
      contact=openapi.Contact(email="mbranko@uns.ac.rs"),
      license=openapi.License(name="GPL v3 License"),
   ),
   public=False,
   permission_classes=(IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', RichTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/publikacije/', include('publikacije.urls', namespace='publikacije')),
    path('api/korpus/', include('korpus.urls', namespace='korpus')),
    path('api/odrednice/', include('odrednice.urls', namespace='odrednice')),
    path('api/render/', include('render.urls', namespace='render')),
    path('api/pretraga/', include('pretraga.urls', namespace='pretraga')),
    path(r'swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

