"""
URL Configuration for CodeVenture.
Maps URL patterns to views with proper error handling.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from WelcomePage.views import home_view
from UserManagement.views import login_view, logout_user

# Main URL patterns
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Django-allauth authentication URLs (includes OAuth providers)
    path('accounts/', include('allauth.urls')),

    # Core application views
    path('', home_view, name="home"),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),

    # Feature modules
    path('register/', include('UserManagement.urls')),
    path('learning/', include('LearningResource.urls')),
    path('quiz/', include('QuizChallengeSystem.urls')),
    path('playground/', include('PythonPlayground.urls')),
    path('progress_tracker/', include('ProgressTracker.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler400 = 'CodeVenture.error_handlers.handler400'
handler403 = 'CodeVenture.error_handlers.handler403'
handler404 = 'CodeVenture.error_handlers.handler404'
handler500 = 'CodeVenture.error_handlers.handler500'
