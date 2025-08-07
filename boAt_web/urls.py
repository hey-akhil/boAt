from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.profile_view, name='profile'),
    path('add-product/', views.add_product, name='add_product'),
    path('view-products/', views.viewProduct, name='viewProduct'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('gift-store/', views.GiftStore, name='gift'),
    path('manage-user/', views.manage_user, name='manage_user'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-user/<int:user_id>/', views.view_user, name='view_user'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('order-success/', views.order_success, name='order_success'),
    path('checkout-cart/', views.checkout_view, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/', views.admin_orders_view, name='admin_orders'),
    # path('admin/orders/<int:order_id>/', views.admin_order_detail_view, name='admin_order_detail'),
    path('update-status/<int:order_id>/', views.update_status, name='update_status'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

