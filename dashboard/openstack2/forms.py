from django import forms
from models import OpenStackAgent

class OpenStackAgentAddForm(forms.Form):
    name = forms.CharField(max_length=128,
                           widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    hostname = forms.GenericIPAddressField(initial='58.247.8.188',
                                           widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    port = forms.IntegerField(initial=40888,
                              widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))

    guest_agent_base_url = forms.GenericIPAddressField(initial='58.247.8.188',
                                           widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))

    def save(self, agent):
        new_agent = OpenStackAgent.objects.create(name=agent.cleaned_data['name'],
                                                  hostname = agent.cleaned_data['hostname'],
                                                  port = agent.cleaned_data['port'])
        new_agent.save()

class OpenStackAgentEditForm(forms.Form):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15', 'readonly':'readonly'}))
    name = forms.CharField(max_length=128,
                           widget=forms.TextInput(attrs={'class': 'form-control m-bot15', 'readonly':'readonly'}))
    hostname = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    port = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))
    guest_agent_base_url = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class': 'form-control m-bot15'}))

    def save(self, agent):
        data = agent.cleaned_data
        agent = OpenStackAgent.objects.get(pk=data['id'])
        agent.__dict__.update(data)
        agent.save()
