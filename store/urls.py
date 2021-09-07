from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_products_view, name='customer-products-view'),
    path('product-details/<int:pk>/', views.customer_product_details, name='customer-product-details'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),

    path('profile/', views.profile, name='profile'),

    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('inbox/', views.admin_inbox, name='inbox'),
    path('message/<str:pk>/', views.message_page, name='message'),
    path('send-feedback/', views.send_feedback, name='send-feedback'),
    path('feedbacks/', views.view_feedback, name='feedbacks'),

    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    path('view-customer/', views.admin_customer_view, name='admin-view-customer'),
    path('delete-customer/<str:username>/', views.admin_customer_delete, name='admin-delete-customer'),

    path('admin-products/', views.admin_products_view, name='admin-products-view'),
    path('add-product', views.admin_add_product, name='add-product'),
    path('admin-product-details/<int:pk>/', views.admin_product_details, name='admin-product-details'),
    path('update-product/<int:pk>/', views.admin_update_product, name='update-product'),
    path('delete-product/<int:pk>/', views.admin_delete_product, name='delete-product'),
]
