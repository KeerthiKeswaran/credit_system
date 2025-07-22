from django.urls import path
from .views import register_customer, check_eligibility, create_loan, get_customer_loans, loan_summary, update_loan_repayment

urlpatterns = [
    path('register/', register_customer),
    path('check-eligibility/', check_eligibility),
    path('create-loan/', create_loan), 
    path('loans/<int:customer_id>/', get_customer_loans, name='get_customer_loans'),
    path('loan-summary/<int:customer_id>/', loan_summary, name='loan_summary'),
    path('update-loan/<int:loan_id>/', update_loan_repayment, name='update_loan'),
]

