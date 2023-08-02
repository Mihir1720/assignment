from django.urls import path
from assets.views import AssetTypesHandler, AssetsHandler, DownloadAssetsHandler

urlpatterns = [
    path("asset-type", AssetTypesHandler.as_view(), name="asset-type"),
    path("assets", AssetsHandler.as_view(), name="assets"),
    path("assets/download", DownloadAssetsHandler.as_view(), name="download-assets")
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)