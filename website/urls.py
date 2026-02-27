from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('toggle_status/<int:pk>', views.toggle_record_status, name='toggle_status'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    
    # Call history
    path('add_call/<int:pk>', views.add_call_history, name='add_call'),
    path('delete_call/<int:call_id>/<int:pk>', views.delete_call, name='delete_call'),
    
    # Email
    path('add_email/<int:pk>', views.add_email, name='add_email'),
    
    # Tasks
    path('add_task/<int:pk>', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/<int:pk>', views.delete_task, name='delete_task'),
]
