from rest_framework.decorators import api_view

from django.utils.timezone import now
from rest_framework.response import Response
from .serializers import UserSerializer, CompanySerializer
from users.models import User, Company


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/company'},
        {'GET': '/api/company/id'},
        {'GET': '/api/company/id/noplanuser'},
        {'GET': '/api/company/id/paiduser'},
        {'GET': '/api/company/id/nonpaiduser'},
        {'GET': '/api/company/id/user/id/charge'},
        {'GET': '/api/company/id/user/id/cancel'},
    ]
    return Response(routes)


@api_view(['GET'])
def getCompany(request):
    company = Company.objects.all()
    serializer = CompanySerializer(company, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCompanyUsers(request, pk):
    company = Company.objects.get(id=pk)
    users = User.objects.filter(company=company)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCompanyUsersWithNoPlan(request, pk):
    company = Company.objects.get(id=pk)
    users = User.objects.filter(company=company).filter(plan__isnull=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCompanyPaidUsers(request, pk):
    company = Company.objects.get(id=pk)
    users = User.objects.filter(company=company).filter(plan__isnull=False)
    users = [x for x in users if x.paiduser]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCompanyNonPaidUsers(request, pk):
    company = Company.objects.get(id=pk)
    users = User.objects.filter(company=company).filter(plan__isnull=False)
    users = [x for x in users if x.paiduser == False]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def chargeCompanyUser(request, pk1, pk2):
    company = Company.objects.get(id=pk1)
    user = User.objects.filter(company=company).filter(
        plan__isnull=False).get(id=pk2)
    if user.payment_done == False or now().month != user.updated.month:
        if user.plan == "Bronze" and user.available_balance >= 500:
            user.available_balance -= 500
            user.payment_done = True
            user.save()
            message = "Payment Done, refresh page to see update"
        elif user.plan == "Silver" and user.available_balance >= 750:
            user.available_balance -= 750
            user.payment_done = True
            user.save()
            message = "Payment Done, refresh page to see update"
        elif user.plan == "Gold" and user.available_balance >= 1500:
            user.available_balance -= 1500
            user.payment_done = True
            user.save()
            message = "Payment Done, refresh page to see update"
        else:
            message = "Payment cannot be done due to insufficient balance, you can cancel the data plan or notify the user about it"
    else:
        message = "The data plan payment is done for this month"

    return Response(message)


@api_view(['GET'])
def cancelDataPlan(request, pk1, pk2):
    company = Company.objects.get(id=pk1)
    user = User.objects.filter(company=company).get(id=pk2)
    user.plan = None
    user.save()
    return Response(f"{user.name}'s data plan has been canceled. Refresh page to see update")
