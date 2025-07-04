from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('items/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('computers/', views.computer_list, name='computer_list'),
    path('computers/add/', views.add_computer, name='add_computer'),
    path('computers/<int:pk>/', views.computer_detail, name='computer_detail'),
    path('computers/<int:pk>/edit/', views.edit_computer, name='edit_computer'),
    path('computers/export/csv/', views.export_computers_csv, name='export_computers_csv'),
    path('computers/export/csv/<str:room>/', views.export_computers_csv, name='export_computers_csv_room'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('work-orders/', views.work_order_request_list_and_add, name='work_order_request_list_and_add'),
    path('work-orders/add/', views.work_order_request_create, name='work_order_request_create'),
    path('work-orders/add/<int:item_id>/', views.work_order_request_create, name='work_order_request_create_for_item'),
    path('work-orders/<int:pk>/delete/', views.delete_work_order_request, name='delete_work_order_request'),
    path('work-orders/<int:pk>/edit/', views.update_work_order_request, name='update_work_order_request'),
    path('work-orders/<int:pk>/export_docx/', views.export_work_order_docx, name='export_work_order_docx'),
]