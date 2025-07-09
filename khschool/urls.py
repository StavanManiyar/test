from django.urls import path
from. import views
urlpatterns = [
    path('', views.home,name='home'),
    path('gallery/',views.gallery,name='gallery'),
    path('contact/',views.contact,name='contact'),
    path('brief/',views.brief,name='brief'),
    path('aboutSchool/',views.aboutSchool,name='aboutSchool'),
    path('chandkheda/',views.chandkheda,name='chandkheda'),
    path('chattral/',views.chattral,name='chattral'),
    path('iffco/',views.iffco,name='iffco'),
    path('kadi/',views.kadi,name='kadi'),
    
    # Additional standard pages
    path('about/', views.aboutSchool, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('facilities/', views.facilities, name='facilities'),
    path('activities/', views.activities, name='activities'),
    path('celebrations/', views.celebrations, name='celebrations'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('our-team/', views.our_team, name='our_team'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('achievements/', views.achievements, name='achievements'),
    
    # Additional template pages
    path('blog/', views.blog, name='blog'),
    path('campus-gallery/', views.campus_gallery, name='campus_gallery'),
    path('carousel/', views.carousel, name='carousel'),
    path('gallery-new/', views.gallery_new, name='gallery_new'),
    path('institutional-goals/', views.institutional_goals, name='institutional_goals'),
    path('team/', views.team, name='team'),
    
    # Campus gallery URLs
    path('chandkheda/photos/',views.chandkheda_gallery_view,name='chandkheda_gallery'),
    path('chattral/photos/',views.chattral_gallery_view,name='chattral_gallery'),
    path('iffco/photos/',views.iffco_gallery_view,name='iffco_gallery'),
    path('kadi/photos/',views.kadi_gallery_view,name='kadi_gallery'),
    
    path('image-test/',views.image_test,name='image_test'),
]

