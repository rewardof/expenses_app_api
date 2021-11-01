from django.db.models import Sum
from django.shortcuts import render
from rest_framework.reverse import reverse
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import AddUserExpenseSerializer
from .models import UserExpense
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from expense import custompermissions


class AddUserExpenseView(ModelViewSet):
    serializer_class = AddUserExpenseSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserExpense.objects.all()
    name = 'add_user_expense'

    def list(self, request, *args, **kwargs):
        data = {}
        queryset = self.get_queryset().filter(user=request.user)
        total_expense = queryset.aggregate(total_expense=Sum('price'))
        serializer = AddUserExpenseSerializer(queryset, many=True)
        data.update(total_expense)
        data['expenses_list'] = serializer.data
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    permission_classes = (
        custompermissions.IsCurrentUserOwner,
    )


@api_view(http_method_names=['GET'])
@permission_classes([custompermissions.IsCurrentUserOwner])
def expense_list(request):
    name = 'expense-list'
    queryset = UserExpense.objects.all()
    serializer = AddUserExpenseSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)


# class ApiRoot(GenericAPIView):
#     name = 'api-root'
#
#     def get(self, request, *args, **kwargs):
#         return Response({
#             # 'add_user_expense': reverse(AddUserExpenseView.name, request=request),
#             'expense_list': reverse('expense_list', request=request)
#
#         })


