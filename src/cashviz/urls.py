"""hellcash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .budget.urls import urlpatterns as budget_urlpatterns
from .costcenter.urls import urlpatterns as costcenter_urlpatterns
from .home.views import Home
from .importer.urls import urlpatterns as importer_urlpatterns
from .journal.urls import urlpatterns as journal_urlpatterns
from .person.urls import urlpatterns as person_urlpatterns
from .spending.urls import urlpatterns as spending_urlpatterns

urlpatterns = [
    path("", Home.as_view(), name="home"),
    *spending_urlpatterns,
    *person_urlpatterns,
    *budget_urlpatterns,
    *costcenter_urlpatterns,
    *journal_urlpatterns,
    *journal_urlpatterns,
    *importer_urlpatterns,
]
