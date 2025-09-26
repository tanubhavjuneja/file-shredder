from django.contrib import admin
from django.urls import path
from users import views as user_views
from discussions import views as disc_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', user_views.register_user, name='register'),
    path('api/login/', user_views.login_user, name='login'),
    path('api/user/', user_views.current_user),
    path('api/discussions/list', disc_views.list_discussions),
    path('api/discussions/create', disc_views.create_discussion),
]
