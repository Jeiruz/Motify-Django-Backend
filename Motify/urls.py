from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Accounts.urls')),
    path('', include('Profile.urls')),
    path('', include("Comments.urls")),
    path('', include("Chat.urls")),
    path('', include("Posts.urls")),
    path('', include("Search.urls"))

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)