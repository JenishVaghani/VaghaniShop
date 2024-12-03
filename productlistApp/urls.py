from django.urls import path
from .import views

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


urlpatterns = [
    # signup, otp, login
    path('signup/', views.signup, name="signup"),
    path('otp/', views.otp, name="otp"),
    path('login/', views.login, name="login"),

    # productadmin
    path('productadmin/', views.productadmin, name="productadmin"),
    path('editproduct/<int:product_id>/', views.edit, name='edit'),
    path('deleteproduct/<int:product_id>/', views.delete, name='delete'),
    path('addproduct/', views.add, name='add'),

    # productshow
    path('productshow/', views.productshow, name="productshow"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('add_to_cart_store/', views.add_to_cart_store, name="add_to_cart_store"),
    path('checkout/', views.checkout, name="checkout"),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),

    # path('payment/', views.payment, name="payment"),
    path("create_payment/", views.create_payment, name="create_payment"),
    path('payment-success', lambda request: HttpResponse("Payment successful!")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)