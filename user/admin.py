from django.contrib import admin

from .models import User, Role, UserRole, Family, Profile
from expense.models import UserExpense

#
# class UserExpenseData(admin.TabularInline):
#     model = UserExpense


# def get_user_expenses(object):
#     print(object)
#     return object.user.userexpense_set.all()


# def book_author(object):
#     return object

@admin.display(description='Expenses')
def get_user_expense(obj):
    list = []
    j = 0
    queryset = obj.userexpense_set.all()
    for i in queryset.iterator():
        j = j + 1
        list.append((j, i.items))
    return list

# class UserExpenseInline(admin.TabularInline):
    # model = UserExpense
    # fields = ('items', 'price', 'description')


class UserAdmin(admin.ModelAdmin):
    model = User
    # inlines = (UserExpenseInline,)
    readonly_fields = (get_user_expense, 'id')


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Family)
admin.site.register(Profile)
