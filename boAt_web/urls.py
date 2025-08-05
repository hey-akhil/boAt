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
    # path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

