from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user", include("userApp.urls")),
    path("", include("videosApp.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
