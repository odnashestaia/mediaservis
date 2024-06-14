from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from videosApp.views import register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("videosApp.urls")),  # добавляем приложение videosApp
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # добавляем приложение для работы с аккаунтом
    path("register/", register, name="register"),
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
