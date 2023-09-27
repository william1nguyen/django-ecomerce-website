from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('view_login/', views.get_login_view, name="view_login"),
    path('view_signup/', views.get_signup_view, name="view_signup"),
    path('create_user/', views.create_user, name="create_user"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
]
