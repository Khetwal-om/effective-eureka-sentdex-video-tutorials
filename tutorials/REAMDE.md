#  sentdex Tutorial


1. python manage.py startapp main , make sure tinymce is installed

2. add urls.py and connect it with project urls

```python

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('',include('tinymce.urls')),

]



```

```python
from django.urls import path
from .views import homepage
urlpatterns = [
    path('',homepage,name='homepage'),
]



```


3. Add Tutorial model 

```python
from django.db import models
from datetime import datetime
# Create your models here.







class Tutorial(models.Model):
    tutorial_title=models.CharField(max_length=200)
    tutorial_content=models.TextField()
    tutorial_published=models.DateTimeField("date published",default=datetime.now())


    def __str__(self):
        return self.tutorial_title
```



4. views.py

```python
from django.shortcuts import render
from .models import Tutorial


# Create your views here.
def homepage(request):
    tutorials=Tutorial.objects.all()
    return render(request,'main/home.html',{'tutorials':tutorials})
```

5. home.html

```html


<html lang="en">
<head>
    <title>hi</title>
{% load static %}
<link href="{%  static 'tinymce/css/prism.css' %}" rel="stylesheet">
</head>

<body>
 {% for tutorial in tutorials %}

 <p>   {{ tutorial.tutorial_title }}</p>
    <p>     {{ tutorial.tutorial_content|safe }}</p>
    <p>{{ tutorial.tutorial_published }}</p>

{% endfor %}
</body>

<script src="{% static 'tinymce/js/prism.js' %}"></script>
</html>
```



# Styling


1. header.html

```html


<html lang="en">
<head>
    <title>hi</title>
{% load static %}

    <link href="{%  static 'tinymce/css/prism.css' %}" rel="stylesheet">
    <link href="{%  static 'main/css/materialize.css' %}" rel="stylesheet">


    <!-- Compiled and minified CSS -->
{#    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">#}

    <!-- Compiled and minified JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</head>

<body>


  <nav>
    <div class="nav-wrapper">
      <a href="#" class="brand-logo">Logo</a>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><a href="{% url 'homepage' %}">Sass</a></li>
        <li><a href="{% url 'homepage' %}">Components</a></li>
        <li><a href="{% url 'homepage' %}">JavaScript</a></li>
      </ul>
    </div>
  </nav>

{% block content %}
{% endblock %}



</body>

<script src="{% static 'tinymce/js/prism.js' %}"></script>

</html>
```



2 home.html


```html
{% extends 'main/header.html' %}


{% block content %}

  <div class="row">

   {% for tutorial in tutorials %}
    <div class="col s12 m6 l4">
      <div class="card blue-grey darken-1">
        <div class="card-content white-text">
          <span class="card-title">{{ tutorial.tutorial_title }}</span>
            <p style="font-size:69%"> {{ tutorial.tutorial_published }}</p>
          <p>{{ tutorial.tutorial_content|safe }}</p>
        </div>
        <div class="card-action">
          <a href="#">This is a link</a>
        </div>
      </div>
    </div>
       {% endfor %}
  </div>


{% endblock %}

```











# User Registration

---

1. register.html

```html

{% extends 'main/header.html' %}

{% block content %}
    <form method="post">
      {% csrf_token %}
        {{ form.as_p }}
        <button class="btn" style="background-color: teal;">Signup</button>
    </form>


{% endblock %}
```


2. register view

```python
from django.shortcuts import render,redirect
from .models import Tutorial
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate


def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid:
            user=form.save()
            login(request,user)
            return redirect('homepage')

        else:
            for sms in form.error_messages:
                print(form.error_messages[sms])
    form=UserCreationForm
    return render(request,'main/register.html',context={'form':form})



```


3. 

---



# Messages


---

1. in views.py

```python


from django.contrib import messages


def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
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
    form=UserCreationForm
    return render(request,'main/register.html',context={'form':form})



```


2. messages.html


```html

        <script>M.toast({html:"{{ message }}",classes:'blue rounded'})</script>

    {% if messages  %}
        {% for message in messages %}
            <script>M.toast({html:"{{ message }}",classes:'blue rounded'})</script>
        {% endfor %}
    {% endif %}
```


---



# User authentication login and logout

1. views

```python



from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate


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



```



2. urls


```python
from django.urls import path
from .views import homepage,register,logout_request,login_request


urlpatterns = [

    path('',homepage,name='homepage'),
    path('register/',register,name='register'),
    path('logout/',logout_request,name='logout'),
    path('login/',login_request,name='login'),
]

```


3. login.html 


```html
{% extends 'main/header.html' %}

{% block content %}
    <form method="post">
      {% csrf_token %}
        {{ form.as_p }}
        <button class="btn" style="background-color: teal;">Login</button>
    </form>


{% endblock %}
```



## Extending the UserCreationForm


1. Add the forms.py 


> A new email field is added in the form

```python
from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User



class NewUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=('username','email','password1','password2')


    def save(self, commit=True):
        user=super(NewUserForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user


```




2. This is what our view looks like now

```python
from django.shortcuts import render,redirect
from .models import Tutorial
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login,logout,authenticate

from django.contrib import messages


# Create your views here.
def homepage(request):
    tutorials=Tutorial.objects.all()
    return render(request,'main/home.html',{'tutorials':tutorials})



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


```
    
    
   
   

# Woooooooooohhhhhhooooooooooooooooo  

## Categories
### Series
#### Tutorial


1. models.py

```python
from django.db import models
from datetime import datetime


class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(TutorialCategory,default=1,verbose_name='Category',
                                          on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField("date published", default=datetime.now())

    tutorial_series = models.ForeignKey(TutorialSeries,default=1, verbose_name='Series',on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200)

    def __str__(self):
        return self.tutorial_title

```





### Now we must display the categories in the homepage rather than all the turorials this is intuitive


1. views

```python
from .models import Tutorial,TutorialCategory,TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse

def single_slug(request,single_slug):
    categories=[c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        return HttpResponse('f{single_slug} is a category')

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in categories:
        return HttpResponse('f{single_slug} is a category')

    return HttpResponse(f'{single_slug} does not exist')




# Create your views here.
def homepage(request):
    return render(request,'main/categories.html',{'categories':TutorialCategory.objects.all()})


```


2. categories.html

```html
{% extends 'main/header.html' %}


{% block content %}


  <div class="row">

   {% for cat in categories %}
      <div class="col s12 m6 l4">
        <a href="{{ cat.category_slug }}" style="color:#000">
            <div class="card hoverable">
                <div class="card-content">
                    <div class="card-title">{{ cat.tutorial_category }}</div>
                    <p>{{ cat.category_summary }}</p>
                </div>
            </div>
        </a>

      


      </div>

       {% endfor %}
  </div>


{% endblock %}

```


3. Add this and boom! it'w working


```python
from django.urls import path
from .views import homepage,register,logout_request,login_request,single_slug


urlpatterns = [

    path('',homepage,name='homepage'),
    path('register/',register,name='register'),
    path('logout/',logout_request,name='logout'),
    path('login/',login_request,name='login'),
    path('<single_slug>',single_slug,name='single_slug'),


]





```

4. Some minor changes 


```python
from .models import Tutorial,TutorialCategory,TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse

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
        return HttpResponse(f'{single_slug} is a tutorial!!!')

    return HttpResponse(f'{single_slug} does not exist')


```



2. Category.html

```html
{% extends 'main/header.html' %}


{% block content %}

  <div class="row">
   {% for tut,partone in part_ones.items %}
      <div class="col s12 m6 l4">
        <a href="{{ partone }}" style="color:#000">
            <div class="card hoverable">
                <div class="card-content">
                    <div class="card-title">{{ tut.tutorial_series }}</div>
                    <p>{{ tut.series_summary }}</p>
                </div>
            </div>
        </a>
      </div>
       {% endfor %}
  </div>


{% endblock %}

```




# Dynamic Sidebar

---

> Before it just make sure the tutorial page is displayed

1. views

```python
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
        return render(request,'main/tutorial.html',{'tutorial':this_tutorial})


    return HttpResponse(f'{single_slug} does not exist')



```


2. tutorial.html

```html
{% extends 'main/header.html' %}

{% block content %}

    <div class="row">
        <div class="col s12, m8, l8">
            <h3>{{tutorial.tutorial_title}}</h3>
            <p style="font-size:70%">Published {{tutorial.tutorial_published}}</p>
            {{tutorial.tutorial_content|safe}}
        </div>
    </div>

{% endblock %}
```




---