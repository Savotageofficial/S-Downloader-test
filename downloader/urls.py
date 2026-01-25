from django.urls import path

from downloader import views

urlpatterns = [
    path("" , views.home , name="downloader"),
    path("download_options/" , views.show_download_options , name="show_download_options"),
    path("download/" , views.download , name="download"),
]