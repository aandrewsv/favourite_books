from django.urls import path
from . import views
                    
urlpatterns = [
    path('books', views.books),
    path('addbook', views.addbook),
    path('newfavorite', views.newfavorite),
    path('unfavorite', views.unfavorite),
    path('books/<int:idn>', views.showbook),
    path('updatebook/<int:idn>', views.updatebook),
    path('areyousure/<int:idn>', views.areyousure),
    path('deletebook', views.deletebook),
    ]