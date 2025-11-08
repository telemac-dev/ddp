from django.urls import path, re_path
from . import views
from .views_temp import temp_view

app_name = 'accounts'

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
    
    # Gerenciamento de usuários (staff only)
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    
    # URLs temporárias - Será removido quando as URLs reais forem implementadas
    re_path(r'^temp/(?P<path>.*)$', temp_view, name='temp_view'),
]
