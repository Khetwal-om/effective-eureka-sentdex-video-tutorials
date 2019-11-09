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

1. 




---