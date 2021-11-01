from .models import UserExpense
from rest_framework.serializers import ModelSerializer


class AddUserExpenseSerializer(ModelSerializer):

        class Meta:
            model = UserExpense
            fields = ('items', 'price', 'category', 'description',)
            read_only_fields = ('user',)


