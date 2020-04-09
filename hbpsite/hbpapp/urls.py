from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('Transactions/', views.TransactionsListView.as_view(), name='transactions'),
    path('trans/', views.trans, name='trans'),
    path('rem_duples/', views.rem_duples, name='rem_duples'),
    path('upload/<int:pk>', views.file_view, name='file_view'),
    path('upload/', views.upload_file, name='upload_file'),
]
