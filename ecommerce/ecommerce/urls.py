
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('benefits/', views.benefits, name="benefits"),
    path('contacts/', views.contactsView, name='contacts'),
    path('success/', views.successView, name="success"),
    path('store/', include('store.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("django.contrib.auth.urls")),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)