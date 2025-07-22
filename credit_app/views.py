from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from datetime import date
import math
from dateutil.relativedelta import relativedelta
from .serializers import RegisterSerializer, CustomerResponseSerializer,EligibilityCheckSerializer, LoanSerializer


@api_view(['POST'])
def register_customer(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        approved_limit = round((36 * data['monthly_income']) / 100000) * 100000

        customer = Customer.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            monthly_salary=data['monthly_income'],
            approved_limit=approved_limit,
            phone_number=data['phone_number']
        )

        response = CustomerResponseSerializer(customer)
        return Response(response.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    serializer = EligibilityCheckSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            customer = Customer.objects.get(id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        P = data['loan_amount']
        R = data['interest_rate'] / (12 * 100)
        N = data['tenure']

        emi = (P * R * math.pow(1 + R, N)) / (math.pow(1 + R, N) - 1)
        emi = round(emi, 2)

        if data['loan_amount'] <= customer.approved_limit:
            return Response({
                "customer_id": customer.id,
                "approval": True,
                "interest_rate": data['interest_rate'],
                "tenure": data['tenure'],
                "monthly_installment": emi,
                "message": "Eligible for the requested loan"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "customer_id": customer.id,
                "approval": False,
                "interest_rate": data['interest_rate'],
                "tenure": data['tenure'],
                "monthly_installment": emi,
                "message": "Loan amount exceeds approved limit"
            }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
    try:
        customer = Customer.objects.get(id=request.data.get("customer_id"))
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loan_amount = float(request.data.get("loan_amount"))
    interest_rate = float(request.data.get("interest_rate"))
    tenure = int(request.data.get("tenure"))  # in months

    # EMI Calculation
    monthly_interest = interest_rate / (12 * 100)
    emi = (loan_amount * monthly_interest * ((1 + monthly_interest) ** tenure)) / (((1 + monthly_interest) ** tenure) - 1)
    emi = round(emi, 2)

    # Set start and end dates
    start_date = date.today()
    end_date = start_date + relativedelta(months=tenure)

    # Create loan
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure,
        monthly_installment=emi,
        emis_paid_on_time=0,
        start_date=start_date,
        end_date=end_date
    )

    serializer = LoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_customer_loans(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def loan_summary(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)

    total_loans = loans.count()
    total_amount_paid = 0
    total_emis_left = 0
    remaining_principal = 0

    for loan in loans:
        paid = loan.emis_paid_on_time * loan.monthly_installment
        remaining_months = loan.tenure - loan.emis_paid_on_time
        remaining_amt = remaining_months * loan.monthly_installment

        total_amount_paid += paid
        total_emis_left += remaining_months
        remaining_principal += remaining_amt

    data = {
        "customer_id": customer.id,
        "name": f"{customer.first_name} {customer.last_name}",
        "total_loans": total_loans,
        "total_amount_paid": round(total_amount_paid, 2),
        "total_emis_left": total_emis_left,
        "remaining_principal": round(remaining_principal, 2)
    }

    return Response(data)

@api_view(['POST'])
def update_loan_repayment(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    paid_emis = request.data.get('emis_paid_on_time')

    if paid_emis is None or not isinstance(paid_emis, int) or paid_emis < 0:
        return Response({'error': 'Invalid or missing emis_paid_on_time'}, status=status.HTTP_400_BAD_REQUEST)

    if paid_emis > loan.tenure:
        return Response({'error': 'EMIs paid cannot exceed total tenure'}, status=status.HTTP_400_BAD_REQUEST)

    loan.emis_paid_on_time = paid_emis
    loan.save()

    return Response({'message': f'Loan {loan_id} updated successfully with {paid_emis} EMIs paid'})



