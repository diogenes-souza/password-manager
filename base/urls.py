from django.urls import path
from .views import passwordList, passwordDetail, passwordCreate, passwordUpdate, DeleteView, CustomLoginView, registerPage, passwordReorder
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', registerPage.as_view(), name='register'),
    path('', passwordList.as_view(), name='passwords'),
    path('password/<int:pk>/', passwordDetail.as_view(), name='password'),
    path('password-create/', passwordCreate.as_view(), name='password-create'),
    path('password-update/<int:pk>/', passwordUpdate.as_view(), name='password-update'),
    path('password-delete/<int:pk>/', DeleteView.as_view(), name='password-delete'),
    path('password-reorder/', passwordReorder.as_view(), name='password-reorder'),

    path('expJson', views.expJson, name='expJson'),
]
