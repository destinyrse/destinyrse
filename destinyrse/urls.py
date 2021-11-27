from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
import app.views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.home, name="home"),
    path('services/', app_views.services, name="services"),
    path('register/', app_views.register, name="register"),
    path('login/', app_views.login_user, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('ajax/check_email/', app_views.check_email, name="check_email"),
    path('ajax/create_test/', app_views.create_test, name="create_test"),
    path('ajax/delete_test/', app_views.delete_test, name="delete_test"),
    path('ajax/create_question/', app_views.create_question, name="create_question"),
    path('ajax/update_ga_client_id/', app_views.update_ga_client_id, name="update_ga_client_id"),
    path('dashboard/', app_views.dashboard, name="dashboard"),
    path('dashboard/nmc/nmc_practice_questions/', app_views.nmc_practice_questions, name="nmc_practice_questions"),
    path('dashboard/nmc/nmc_practice_questions/take_test/<int:id>/', app_views.take_test, name="take_test"),
    path('dashboard/admin/', app_views.admin, name="dashboard_admin"),
    path('dashboard/admin/nmc/upload_questions/', app_views.upload_nmc, name="upload_nmc"),
    path('dashboard/admin/nmc/view_test/<int:id>/', app_views.view_test, name="view_test"),
    path('dashboard/admin/nmc/edit_question/<int:id>/', app_views.edit_question, name="edit_question"),
]
