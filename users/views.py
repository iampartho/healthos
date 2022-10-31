from django.shortcuts import render, redirect
from .models import Company, User
from .forms import ChangePlanForm, CustomUserCreationForm
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required

from .utils import number_verification, verify_secondary_numbers
# Create your views here.


def home(request):
    all_company = Company.objects.all()
    return render(request, "user/home.html", context={'company': all_company})


def company_detail(request, pk):
    company = Company.objects.get(id=pk)
    users = User.objects.filter(company=company)
    return render(request, "user/company_detail.html", context={'users': users})


@login_required(login_url='login')
def account(request):
    user = request.user
    if user.payment_done and now().month == user.updated.month:
        payment_done = True
    elif user.updated.month > now().month:
        user.payment_done = False
        payment_done = False
        user.save()
    else:
        payment_done = False

    return render(request, 'user/user-account.html', context={'user': user, 'payment_done': payment_done})


@login_required(login_url='login')
def change_plan(request):
    user = request.user
    form = ChangePlanForm(instance=user)
    if request.method == 'POST':
        form = ChangePlanForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if user.plan == "Gold" and user.available_balance > 1500:
                user.available_balance -= 1500
                user.payment_done = True
                user.save()
                return redirect('account')
            elif user.plan == 'Silver' and user.available_balance > 750:
                user.available_balance -= 750
                user.payment_done = True
                user.save()
                return redirect('account')
            elif user.plan == 'Bronze' and user.available_balance > 500:
                user.available_balance -= 500
                user.payment_done = True
                user.save()
                return redirect('account')
            else:
                messages.error(
                    request, 'There was a problem processing your request! Please check your available balance and check the plan you choose and do it again')
                return redirect('change-plan')
    context = {'form': form}
    return render(request, 'user/change-plan.html', context)


@login_required(login_url='login')
def plan_cancelation(request):
    user = request.user
    if user.plan == "Gold":
        user.plan = None
        user.save()
    else:
        messages.error(
            request, 'You cannot cancel plan with having Silver or Bronze plan. Upgrade to Gold to have cancellation feature.')
    return redirect('account')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        password = request.POST['password']

        try:
            user = User.objects.get(primary_phone_number=phonenumber)
        except:
            messages.error(request, 'Phonenumber does not exist')

        user = authenticate(
            request, primary_phone_number=phonenumber, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Phonenumber OR password is incorrect')

    return render(request, 'user/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('home')


def registerUser(request):

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            primary_number = request.POST.get('primary_phone_number')

            if number_verification(primary_number):
                user.primary_phone_number = primary_number
                user.username = user.primary_phone_number
            else:
                messages.error(
                    request, 'Please enter an appropriate primary contact number')
                return redirect('register')

            secondary_input_numbers = request.POST.get(
                'secondary_numbers').replace(',', " ").split()
            secondary_numbers = verify_secondary_numbers(
                secondary_input_numbers)
            if len(secondary_numbers) == len(secondary_input_numbers):
                user.secondary_number_field = ' '.join(secondary_numbers)
            else:
                messages.error(
                    request, 'Please enter the secondary numbers appropriately')
                return redirect('register')

            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'user/register.html', context)
