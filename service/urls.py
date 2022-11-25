from django.urls import path

from service.views import item_by_id, buy_by_id,  home, stripe_config, \
    create_checkout_session


urlpatterns = [
    path('', home, name="home"),
    path('config/', stripe_config),

    path('create-checkout-session/', create_checkout_session),


    path('item/id=<int:item_id>', item_by_id, name="item_by_id"),
    # path('buy/id=<int:item_id>', buy_by_id, name="buy_by_id"),

    # path('buy/id=<int:item_id>', create_stripe_checkout_session, name="buy_by_id"),


]
