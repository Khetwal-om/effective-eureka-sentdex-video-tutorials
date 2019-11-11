from django.shortcuts import render,redirect
from .models import Tutorial,TutorialCategory,TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse


from . models import Moments





def single_slug(request,single_slug):

    categories=[c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series=TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)

        series_urls={}
        for m in matching_series.all():
            part_one=Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest('tutorial_published')
            series_urls[m]=part_one.tutorial_slug

        return render(request,'main/category.html',{'part_ones':series_urls})

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial=Tutorial.objects.get(tutorial_slug=single_slug)

        tutorials_from_series=Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by('tutorial_published')
        this_tutorial_idx=list(tutorials_from_series).index(this_tutorial)



        return render(request,'main/tutorial.html',{'tutorial':this_tutorial,'sidebar':tutorials_from_series,'this_tutorial_idx':this_tutorial_idx})

    return HttpResponse(f'{single_slug} does not exist')




# Create your views here.
def homepage(request):
    moments=Moments.objects.all()

    return render(request,'main/categories.html',{'categories':TutorialCategory.objects.all(),'moments':moments})



def register(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid:
            user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'account created for {username}')
            login(request,user)
            messages.info(request,f'Now enjoy the party:{username}')
            return redirect('homepage')
        else:
            for sms in form.error_messages:
                messages.error(request,f'{sms}:{form.error_messages[sms]}')
    form=NewUserForm
    return render(request,'main/register.html',context={'form':form})


def logout_request(request):
    logout(request)
    messages.info(request,'Logged out successfully!!!')
    return redirect('homepage')


def login_request(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'you are logged in as {username}')
                return redirect('homepage')
            else:
                messages.error(request,'Invalid username or password')
        else:
            messages.error(request,'Something is wrong ')

    form=AuthenticationForm()
    return render(request,'main/login.html',{'form':form})

