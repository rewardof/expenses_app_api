from django.db import models
from user.models import User


class UserExpense(models.Model):
    EXPENSES_CATEGORY = [
        ('clothes', 'Clothes'),
        ('food', 'Food'),
        ('education', 'Education'),
        ('household_expense', 'Household Expenses'),
        ('electronics', 'Electronics'),
        ('technics', 'Technics'),
        ('sport', 'Sport'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, choices=EXPENSES_CATEGORY)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
        permissions = (
            ('can_view_expenses', 'Grandfather or father can view all family members expenses'),
        )

    def __str__(self):
        return self.items

    def get_name(self):
        return self.items

    def get_absolute_url(self):
        return f"/expenses/list/{self.id}"

    def get_absolute_url_delete(self):
        return f"/expenses/delete/{self.id}"
