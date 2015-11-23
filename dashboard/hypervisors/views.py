from django.views import generic
from models import *

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'hypervisors/index.html'
