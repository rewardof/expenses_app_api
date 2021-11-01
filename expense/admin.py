from django.contrib import admin

from .models import UserExpense, User


class UserExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'items', 'price', 'description')


admin.site.register(UserExpense, UserExpenseAdmin)

