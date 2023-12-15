from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import make_password, check_password
from hitcount.managers import HitCountManager
from hitcount.views import HitCountMixin
from .EmailBackEnd import EmailBackEnd
from .forms import StatusUserForm
from .models import User, Status, Authors, Category,StatusUser
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login
from hitcount.utils import get_hitcount_model


@login_required(login_url='/acc/login')
def index(request):
    category = Category.objects.all()
    status = Status.objects.all()
    page = Paginator(status, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    ctx = {
        'status':status,
        'page':page,
        'category':category
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
    messages.error(request, "You are logout")
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
    category = Category.objects.all()
    product = Status.objects.filter(id=id).last()
    fav = bool

    if product.favourites.filter(id=request.user.id).exists():
        fav = True
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
        'hits':hits,
        'fav':fav,
        'category':category
    }
    return render(request,'status.html',ctx)


def favourite(request, id):
    post = get_object_or_404(Status, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
        messages.error(request, 'Successfuly removed')
    else:
        post.favourites.add(request.user)
        messages.success(request, 'Successfuly')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def sevimli(request):
    category = Category.objects.all()
    new = Status.objects.filter(favourites=request.user)
    page = Paginator(new, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    return render(request, 'favourite.html', {
        'new': new,
        'page':page,
        'category':category
                                              })

def category_filter(request, id):
    category = Category.objects.all()
    page_cat = Category.objects.get(id=id)
    status = Status.objects.filter(category_id=id)
    page = Paginator(status, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    ctx = {
        'status':status,
        "category":category,
        'page':page,
        'page_cat':page_cat
    }

    return render(request,'category.html',ctx)


def statusadd(request):
    category = Category.objects.all()
    if request.user.count:
        if request.method == "POST":
            text = request.POST.get('text')
            status_save = StatusUser(text=text,author=request.user)
            print(status_save)
            request.user.count = False
            request.user.save()
            print("ishladi")
            status_save.save()
            messages.success(request, "Your status has been placed on our site")
            return redirect('index')
    else:
            messages.error(request, "Sorry, your status is limited")
            return redirect('index')



    ctx = {
        'category':category
    }
    return render(request,'status_add.html',ctx)


def users_status(request):
    users = StatusUser.objects.all()
    page = Paginator(users, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    category = Category.objects.all()

    ctx = {
        'page':page,
        'category':category
    }

    return render(request,'users_status.html',ctx)

def users_status_get(request,id):
    users = StatusUser.objects.get(id=id)
    status = StatusUser.objects.get(id=id)

    category = Category.objects.all()
    hit_count = get_hitcount_model().objects.get_for_object(users)
    hits = hit_count.hits
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = + 1
    athor_status = StatusUser.objects.filter(
        Q(author__username__icontains=users.author)
    )
    page = Paginator(athor_status, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    ctx = {
        'page': page,
        'category':category,
        'hits':hits,
        'status':status,
        'athor_status':athor_status,
    }

    return render(request,'users_get.html',ctx)

def my_status(request):
    status = StatusUser.objects.filter(author__username__icontains=request.user.username)
    category = Category.objects.all()
    ctx = {
        'status':status,
        'category':category
    }

    return render(request,'my_status.html',ctx)

@login_required(login_url='login')
def edit(request,id):
    model = StatusUser.objects.get(id=id)
    form = StatusUserForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Your status are Successfully Updated !')
            return redirect('my_status')
    ctx = {
        "form": form
    }


    return render(request, 'edit.html',ctx)

def delete(request, id):
    request.user.count = True
    request.user.save()
    status = StatusUser.objects.get(id=id)
    status.delete()
    messages.success(request, "Your status successfuly deleted")
    return redirect('index')
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
