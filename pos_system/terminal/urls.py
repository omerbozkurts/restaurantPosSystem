from django.urls import include

urlpatterns += [
    path('terminal/', include('terminal.urls')),
]
