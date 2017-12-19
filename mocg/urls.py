"""mocg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import authen.views as authen_view
import csys.views as csys_view

urlpatterns = [
    url(r'^$', authen_view.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', authen_view.login_view),
    url(r'^system/$', authen_view.system_view),
    url(r'^signout/$', authen_view.logout_view),
    url(r'^editing/$', authen_view.edit_user_view),
    url(r'^control/$', authen_view.control_view),
    url(r'^get_users/$', authen_view.users_get_view),
    url(r'^uploadfile/$', csys_view.csys_upload),
    url(r'^handle_data/$', csys_view.csys_handle_data),

]
