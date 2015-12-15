# -*- coding: utf-8 -*-
import json, pprint
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.forms.utils import ErrorList

from django.views.generic import ListView, DetailView, FormView, View, TemplateView