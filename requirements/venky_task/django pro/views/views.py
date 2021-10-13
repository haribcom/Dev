from django.shortcuts import render
from hrb.forms import SignUpForm,bookroom
from django.http import HttpResponseRedirect
from hrb.models import Rooms,hotelusers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.
def home(req):
    return render(req,'hrb/home.html')


def logout_view(request):
    return render(request,'hrb/home.html')

def login(request):
    form=LoginForm()
    response=render(request,'registration/login.html')
    if request.method=='POST':
        name=request.POST['username']
        quantity=request.POST['password']
        request.session[name]=name
        request.session.set_expiry(180)
    return response
def userhome(request):
    Acrooms=Rooms.objects.filter(roomtype='ac',status='available').count()
    NonAc=Rooms.objects.filter(roomtype='nonac',status='available').count()
    visitors=hotelusers.objects.all()
    visitorscount=visitors.count()-1
    paginator=Paginator(visitors,1)
    page_number=request.GET.get('page')
    try:
        visitors=paginator.page(page_number)
    except PageNotAnInteger:
        visitors=paginator.page(1)
    except EmptyPage:
        visitors=paginator.page(paginator.num_pages)

    total=Acrooms+NonAc
    return render(request,'hrb/userhome.html',{'Acrooms':Acrooms,'NonAc':NonAc,'total':total,'visitors':visitors,'visitorscount':visitorscount})

def signup_view(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/accounts/login')
    return render(request,'hrb/signup.html',{'form':form})
def bookroom_view(request):
    Acrooms=Rooms.objects.filter(roomtype='ac',status='available').count()
    NonAc=Rooms.objects.filter(roomtype='nonac',status='available').count()
    visitors=hotelusers.objects.all()
    paginator=Paginator(visitors,7)
    page_number=request.GET.get('page')
    try:
        visitors=paginator.page(page_number)
    except PageNotAnInteger:
        visitors=paginator.page(1)
    except EmptyPage:
        visitors=paginator.page(paginator.num_pages)

    total=Acrooms+NonAc
    form=bookroom()
    response=render(request,'hrb/bookroom.html',{'form':form,'Acrooms':Acrooms,'NonAc':NonAc,'total':total,'visitors':visitors})

    if request.method=='POST':
        form=bookroom(request.POST)
        if form.is_valid():
            alert=1
            form.save()

        else:
            alert=0
    return response
