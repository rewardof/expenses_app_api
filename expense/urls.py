from django.urls import path, include
from expense import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('add_expense', views.AddUserExpenseView, basename='expense')

app_name = 'expense'

urlpatterns = [
    path('expense/', include(router.urls)),
    path('expense_list', views.expense_list, name='expense_list'),
]
