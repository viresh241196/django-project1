from django.shortcuts import render, redirect
from .form import UserRegistrationForm, ProfileRegistrationForm, ProfileUpdateForm, LoginForm, DepositForm, \
    WithdrawForm, transferForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Passbook
from django.contrib.auth.models import User, auth
import time


def home(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        login_form = LoginForm()
    return render(request, 'account/home.html', {'login_form': login_form})


def contact(request):
    return render(request, 'account/contact.html')

#
def about(request):
    return render(request, 'account/about.html')


def base1(request):
    return render(request, 'account/base1.html')


def register1(request):
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('register2')
    else:
        register_form = UserRegistrationForm()
        # data = Profile.objects.last()
        # print(data.account_number)
    return render(request, 'account/register1.html', {'register_form': register_form})


def register2(request):
    if request.method == "POST":
        profile_form = ProfileRegistrationForm(request.POST)
        if profile_form.is_valid():
            user = User.objects.last()
            profile = profile_form.save(commit=False)
            profile.user = user
            new_account = int(update_section())
            profile_form.save()
            pk = user.id
            Profile.objects.filter(user_id=pk).update(email=user.email, name=user.username, account_number=new_account)
            data = Profile.objects.filter(account_number=new_account).first()
            passbook_entry(data, deposit=data.savings)
            username = user.username
            messages.success(request, f'Welcome {username}, your account number is {new_account} ')
            return redirect('home')
    else:
        profile_form = ProfileRegistrationForm()
        #Profile.objects.last()
    return render(request, 'account/register2.html', {'profile_form': profile_form})


def login(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('home')
    else:
        login_form = LoginForm()
    return render(request, 'account/login.html', {'login_form': login_form})


def logout(request):
    auth.logout(request)
    return redirect('home')


def update_section():
    data = Profile.objects.last()
    account_number = data.account_number
    new_account_number = account_number + 1
    return new_account_number


def profile(request):
    if request.method == 'POST':
        update_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if update_profile.is_valid():
            update_profile.save()
            messages.success(request, f'{request.user.username} your profile is updated')
            return redirect('profile')
        else:
            messages.error(request, f" Kindly fill proper data")
            return redirect('profile')
    else:
        update_profile = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'account/profile.html', {'update_profile': update_profile})


def passbook_entry(data, deposit=0, withdraw=0):
    entry = Passbook.objects.create(time=time.ctime(), name=data.name, account_number=data.account_number,
                                    savings=data.savings)
    entry.deposit = deposit
    entry.withdraw = withdraw
    entry.save()
    return


@login_required(login_url='login')
def check_passbook(request):
    name = request.user.profile.name
    account_number = request.user.profile.account_number
    data = Passbook.objects.filter(account_number=account_number)
    return render(request, 'account/passbook.html', {'data': data, 'name': name})


@login_required(login_url="login")
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit_amount = form.cleaned_data.get("deposit")
            account_number = form.cleaned_data.get("account_number")
            data = Profile.objects.filter(account_number=account_number).first()
            if data.name == request.user.profile.name and data.account_number == request.user.profile.account_number:
                new_savings = data.savings + deposit_amount
                pk = data.user_id
                Profile.objects.filter(user_id=pk).update(savings=new_savings)
                data = Profile.objects.filter(account_number=account_number).first()
                passbook_entry(data, deposit=deposit_amount)
                username = data.name
                messages.success(request, f'{username}, your account is credited with {deposit_amount} ')
                return redirect('home')
            else:
                messages.error(request, f'invalid input')
                return redirect('deposit')
    else:
        form = DepositForm()
        return render(request, 'account/deposit.html', {'form': form})


@login_required(login_url="login")
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            withdraw_amount = form.cleaned_data.get("withdraw")
            account_number = form.cleaned_data.get("account_number")
            data = Profile.objects.filter(account_number=account_number).first()
            if data.name == request.user.profile.name and data.account_number == request.user.profile.account_number:
                new_savings = data.savings - withdraw_amount
                pk = data.user_id
                Profile.objects.filter(user_id=pk).update(savings=new_savings)
                data = Profile.objects.filter(account_number=account_number).first()
                passbook_entry(data, withdraw=withdraw_amount)
                username = data.name
                messages.success(request, f'{username}, your account is debited with {withdraw_amount} ')
                return redirect('home')
            else:
                messages.error(request, f'invalid input')
                return redirect('withdraw')
    else:
        form = WithdrawForm()
        return render(request, 'account/withdraw.html', {'form': form})


@login_required(login_url="login")
def transfer(request):
    if request.method == 'POST':
        transfer_form = transferForm(request.POST)
        if transfer_form.is_valid():
            account_1 = transfer_form.cleaned_data.get('account_number_1')
            account_2 = transfer_form.cleaned_data.get('account_number_2')
            amount = transfer_form.cleaned_data.get('amount')
            data_1 = Profile.objects.filter(account_number=account_1).first()
            data_2 = Profile.objects.filter(account_number=account_2).first()
            if data_1.name == request.user.profile.name and data_1.account_number == request.user.profile.account_number\
                    and data_2.account_number == account_2:
                new_savings_1 = data_1.savings - amount
                new_savings_2 = data_2.savings + amount
                pk_1 = data_1.user_id
                pk_2 = data_2.user_id
                Profile.objects.filter(user_id=pk_1).update(savings=new_savings_1)
                Profile.objects.filter(user_id=pk_2).update(savings=new_savings_2)
                data_sender_entry = Profile.objects.filter(account_number=account_1).first()
                data_receiver_entry = Profile.objects.filter(account_number=account_2).first()
                passbook_entry(data_sender_entry, withdraw=amount)
                passbook_entry(data_receiver_entry, deposit=amount)
                username_1 = data_1.name
                username_2 = data_2.name
                messages.success(request, f'{username_1}, {amount} amount is transfer form your account to {username_2} account.')
                return redirect('home')
            else:
                messages.error(request, f'invalid input')
                return redirect('transfer')
    else:
        transfer_form = transferForm()
        return render(request, 'account/transfer.html', {'transfer_form': transfer_form})
