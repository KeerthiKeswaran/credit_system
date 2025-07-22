from rest_framework import serializers
from .models import Customer, Loan 

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    monthly_income = serializers.FloatField()
    phone_number = serializers.CharField(max_length=15)

class CustomerResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    monthly_income = serializers.FloatField(source='monthly_salary')

    class Meta:
        model = Customer
        fields = ['id', 'name', 'age', 'monthly_income', 'approved_limit', 'phone_number']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class EligibilityCheckSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
    
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
