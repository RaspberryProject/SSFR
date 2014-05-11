from django.conf import settings
settings.configure(
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql', 
	        'NAME': 'meal_recipe',
	        'USER': 'root',
	        'PASSWORD': 'raspberry',
	        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
	        'PORT': '3306',
	    }
	}
)