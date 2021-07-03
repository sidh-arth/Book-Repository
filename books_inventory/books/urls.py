from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('book', views.BookViewSet, basename='books')
router.register('borrow', views.BorrowerViewSet, basename='borrow')

urlpatterns = [
	path('register/', views.UserRegistrationView.as_view(), name='auth_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
]

urlpatterns += router.urls