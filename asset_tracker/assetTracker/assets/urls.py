from django.urls import path
from assets.views import AssetTypesHandler, AssetsHandler, DownloadAssetsHandler

urlpatterns = [
    path("asset-type", AssetTypesHandler.as_view(), name="asset-type"),
    path("assets", AssetsHandler.as_view(), name="assets"),
    path("assets/download", DownloadAssetsHandler.as_view(), name="download-assets")
]