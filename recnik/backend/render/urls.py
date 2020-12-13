from django.urls import path
from .views import odrednica_html, odrednice_html, odrednice_pdf

app_name = 'render'

urlpatterns = [
    path('odrednica/', odrednice_html),
    path('odrednica/<int:pk>/', odrednica_html),
    path('pdf/odrednica/', odrednice_pdf),
]
