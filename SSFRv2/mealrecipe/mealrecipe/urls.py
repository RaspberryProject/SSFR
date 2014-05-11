from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mealrecipe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'meal.views.view_meals_suggestion', name='home'),
    url(r'^get_stock$', 'meal.views.show_meal_stock', name='get_stock'),
)
