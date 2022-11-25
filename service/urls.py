from django.urls import path

from service.views import item_by_id, buy_by_id, stripe_config


urlpatterns = [
    path('config/', stripe_config),
    path('item/id=<int:item_id>', item_by_id, name="item_by_id"),
    path('buy/id=<int:item_id>', buy_by_id, name="buy_by_id"),
]
