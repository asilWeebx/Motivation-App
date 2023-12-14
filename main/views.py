from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import make_password, check_password
from hitcount.managers import HitCountManager
from hitcount.views import HitCountMixin
from .EmailBackEnd import EmailBackEnd
from .models import User, Status, Authors
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from hitcount.utils import get_hitcount_model


@login_required(login_url='/acc/login')
def index(request):
    status = Status.objects.all()
    page = Paginator(status, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    ctx = {
        'status':status,
        'page':page
    }



    return render(request,"index.html",ctx)



def my_functional_view(request):
    message = ''
    if request.method == 'POST':

        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(username) < 6:
            message = 'Your username is too short'
        elif User.objects.filter(username=username):
            message = 'This username is already token'
        elif len(email) < 6:
            message = 'Please enter true email address'
        elif User.objects.filter(email=email):
            message = 'You have already an account according to your email address'
        elif len(password1) < 6:
            message = 'The password must contain 6 symbols'
        elif password1 != password2:
            message = "The password don't match"
        else:
            user = get_user_model().objects.create(first_name=name, username=username,
                                                   password=make_password(password1), email=email)

            return redirect('login',)

    return render(request, 'signup.html', {"message": message})


def Logout(request):
    logout(request)
    return redirect('index')

def search(request):
    if request.method == "POST":
        search = request.POST['search']
        status = Status.objects.filter(
            Q(author__full_name__icontains=search)
        )
        print(status)
        return render(request, 'index.html',
                      {'search': search,
                       'status': status})


def status(request,id):
    status = Status.objects.get(id=id)
    hit_count = get_hitcount_model().objects.get_for_object(status)
    hits = hit_count.hits
    hit_count_response = HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits =+ 1
    athor_status = Status.objects.filter(
        Q(author__full_name__icontains=status.author)
    )
    status_count = Status.objects.filter(
        Q(author__full_name__icontains=status.author)
    ).count()
    page = Paginator(athor_status, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    print(athor_status)
    ctx = {
        'status':status,
        'athor_status':athor_status,
        'page':page,
        'status_count':status_count,
        'hits':hits
    }
    return render(request,'status.html',ctx)


"""


USER PAGES END


START ADMIN DASHBOARD


"""

def doLogin(request):
        if request.method == "POST":
            user = EmailBackEnd.authenticate(request, username=request.POST.get('username'),
                                             password=request.POST.get('password'))
            if user != None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, 'ADMIN DASHBOARDGA MARHAMAT')
                    return redirect('dashboard_admin')
                else:
                    messages.error(request, 'Siz SuperUser emassiz!')
                    return redirect('loginn')
            else:
                messages.error(request, 'Parol yoki Username Xato!')
                return redirect('loginn')

        return None


def LOGINN(request):
    return render(request, 'dashboard/login.html')


def dashboard_admin(request):
    if request.user.is_active:
       return render(request,'dashboard/dashboard.html')
    else:
       messages.error(request, 'Siz SuperUser emassiz!')
       return redirect('loginn')

