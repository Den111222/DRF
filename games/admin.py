from django.contrib import admin
from games.models import *

admin.site.register(GameModel)
admin.site.register(GamerModel)
admin.site.register(GamerLibraryModel)