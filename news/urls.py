from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index),
    path('currentdate', views.current_date),
    path('notfound', views.not_found),
    path('permission', views.permission_denied_view),
    path('up', views.upload_file, name='up'),
    path('csvout', views.some_streaming_csv_view),
    path('pdfout', views.pdfgen),
    path('sessiontest', views.sessiontest),
    path('addmess', views.addmess),
]

