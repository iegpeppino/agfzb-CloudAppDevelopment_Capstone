from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from pkg_resources import add_activation_listener
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route = 'about_us/', view = views.about , name = 'about_us'),
    # path for contact us view
    path(route = 'contact_us/', view = views.contact , name = 'contact_us'),
    # path for registration
    path(route = 'registration/', view = views.registration_request , name = 'registration'),
    # path for login
    path(route = 'login/', view = views.login_request , name = 'login'),
    # path for logout
    path(route = 'logout/', view = views.logout_request , name = 'logout'),
    # path for home route
    path(route='', view = views.get_dealerships, name='index'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path('review/<int:dealer_id>/', views.add_review, name='add_review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)