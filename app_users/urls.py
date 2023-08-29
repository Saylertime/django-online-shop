from django.urls import path
from app_users.views import register_view, authview, ProfileUpdateView, ProfileListView, ProfileDetailView, HistoryListView, HistoryDetailView, AccountDetailView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profiles', ProfileListView.as_view(), name='profiles'),
    path('profile/<int:pk>/update', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/history', HistoryListView.as_view(), name='profile-history'),
    path('profile/history/<int:pk>', HistoryDetailView.as_view(), name='history-detail'),
    path('profile/<int:pk>/account', AccountDetailView.as_view(), name='account-detail'),
    path('register', register_view, name='register'),
    path('login', authview, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="app_users/reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="app_users/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="app_users/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="app_users/password_reset_done.html"),
         name='password_reset_complete'),
]