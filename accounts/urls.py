from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #サインアップ画面
    path('register/', views.registerPage, name="register"),
    #ログイン画面
    path('login/', views.loginPage, name="login"),
    #ログアウト
    path('logout/', views.logoutUser, name="logout"),
    #ホーム画面
    path('', views.home, name="home"),
    #ユーザーページ
    path('user/', views.userPage, name="user-page"),
    #ユーザー設定画面
    path('account/', views.accountSettings, name="account"),
    #商品一覧画面
    path('products/', views.products, name="products"),
    #カスタマーページ
    path('customer/<str:pk>', views.customer, name="customer"),
    #注文ページ
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    #注文編集ページ
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    #注文削除ページ
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
