from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from store.utils import cartData, guestOrder, cookieCart

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login' ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout",  kwargs={'next_page': '/'}),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change_form.html", success_url = "done/"), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"), name="password_change_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html", success_url="done/"), name="password_reset"),

    # path('password_reset/', views.password_reset_request, name="password_reset"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = "accounts/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = "accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name = "accounts/password_reset_complete.html"), name="password_reset_complete"),
]
