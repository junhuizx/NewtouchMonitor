from django import forms
from django.core.exceptions import ObjectDoesNotExist
from dashboard.hypervisors.models import *

class HypervisorsAddForm(forms.Form):
    hostname = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    location = forms.ModelChoiceField(queryset=IDC.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    collector =forms.ModelChoiceField(queryset=Collector.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    user =forms.ModelChoiceField(queryset=User.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    snmp_version =forms.ChoiceField(choices=(('1', '1'),('2', '2c'),),
                                    initial=('2', '2c'),
                                    widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    snmp_commit = forms.CharField(max_length=128,
                                  initial='public',
                                  widget=forms.TextInput(attrs={'class': 'form-control placeholder-no-fix',
                                                                'autocomplete':"off",
                                                                 "placeholder":"SNMP COMMIT" }))


    def save(self, hypervisor):
        try:
            Hypervisors.objects.get(hostname=hypervisor.cleaned_data['hostname'], location = hypervisor.cleaned_data['location'])
            raise forms.ValidationError("Already had")
        except ObjectDoesNotExist:
            new_hypervisor = Hypervisors.objects.create(hostname=hypervisor.cleaned_data['hostname'],
                                                        snmp_commit = hypervisor.cleaned_data['snmp_commit'],
                                                        snmp_version = hypervisor.cleaned_data['snmp_version'],
                                                        location = hypervisor.cleaned_data['location'],
                                                        collector = hypervisor.cleaned_data['collector'],
                                                        user = hypervisor.cleaned_data['user'])
            new_hypervisor.save()

class HypervisorsEditForm(forms.Form):
    id = forms.IntegerField(show_hidden_initial=False, widget=forms.TextInput(attrs={'class': 'form-control m-bot15','readonly':'readonly'}))
    hostname = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15','readonly':'readonly'}),
                                           required=False)
    location = forms.ModelChoiceField(queryset=IDC.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15','readonly':'readonly'}),
                                      required=False)
    collector =forms.ModelChoiceField(queryset=Collector.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15'}),
                                      required=False)
    user =forms.ModelChoiceField(queryset=User.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15','readonly':'readonly'}))
    snmp_version =forms.ChoiceField(choices=(('1', '1'),('2', '2c'),),
                                    initial=('2', '2c'),
                                    widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    snmp_commit = forms.CharField(max_length=128,
                                  initial='public',
                                  widget=forms.TextInput(attrs={'class': 'form-control placeholder-no-fix',
                                                                'autocomplete':"off",
                                                                 "placeholder":"SNMP COMMIT" }))
    rules = forms.ModelMultipleChoiceField(required=False,
                                   queryset=HypervisorsRules.objects.all(),
                                   widget=forms.SelectMultiple(attrs={'class': 'form-control placeholder-no-fix'}))
    ssh_username = forms.CharField(max_length=128,
                                   required=False,
                                  initial='root',
                                  widget=forms.TextInput(attrs={'class': 'form-control placeholder-no-fix'}))
    ssh_password = forms.CharField(max_length=128,
                                   required=False,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control placeholder-no-fix'}))
    ssh_password_confirm = forms.CharField(max_length=128,
                                   required=False,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control placeholder-no-fix'}))

    def clean(self):
        '''Required custom validation for the form.'''
        super(forms.Form,self).clean()
        if 'ssh_password' in self.cleaned_data and 'ssh_password_confirm' in self.cleaned_data:
            if self.cleaned_data['ssh_password'] != self.cleaned_data['ssh_password_confirm']:
                self._errors['ssh_password'] = [u'Passwords must match.']
                self._errors['ssh_password_confirm'] = [u'Passwords must match.']
        return self.cleaned_data

    def save(self, hypervisor):
        data = hypervisor.cleaned_data
        hy = Hypervisors.objects.get(pk=data['id'])
        hy.__dict__.update(data)
        hy.save()

class CollertorAddForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15','readonly':'readonly'}))
    name = forms.CharField(max_length=128,
                          widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    user =forms.ModelChoiceField(queryset=User.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-bot15'}))
    key = forms.CharField(max_length=128,
                          widget=forms.TextInput(attrs={'class': 'form-control m-bot15','readonly':'readonly'}))
    hostname = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    port = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))

    def save(self, form):
        form = form.cleaned_data
        try:
            Collector.objects.get(id=form['id'])
            raise forms.ValidationError("Already had")
        except ObjectDoesNotExist:
            collector = Collector.objects.create(id = form['id'],
                                                 name = form['name'],
                                                 key = form['key'],
                                                 user = form['user'],
                                                 hostname = form['hostname'],
                                                 port = form['port'])
            collector.save()

