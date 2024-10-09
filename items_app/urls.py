from django.urls import path
from .views import ItemAPI

urlpatterns = [
    path('', ItemAPI.as_view(), name='item'),
    path('<int:item_id>/', ItemAPI.as_view(), name='item-detail')
]