from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:  # Only include the toolbar if in DEBUG mode
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]