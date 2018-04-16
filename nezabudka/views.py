from lxml import etree
import requests
import json

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Contacts
from .forms import FileUploadModelForm, ContactViewForm
from .rest import *


class ContactsListView(ListView):
    model = Contacts
    paginate_by = 5

    def parsing_site(self):
        r = requests.get("https://breffi.ru/ru/about", verify=False)

        html = etree.HTML(r.text)
        data = html.xpath(".//*[@class='content-section worth']/*\
                         [@class='content-section__layout']/*\
                         [@class='content-section__item']")
        out = []
        for d1 in data:
            out.append((d1.getchildren()[1].text, "".\
                        join([x for x in d1.getchildren()[2].itertext()])))
        return out

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)

        try:
            context['fulldesc'] = self.parsing_site()
        except Exception as e:
            context['fulldesc'] = []
        return context

    def get_queryset(self):
        search = self.request.GET.get('search', None)

        if search == None:
            return Contacts.objects.all()
        else:
            return Contacts.objects.filter(Q(name__icontains=search) | \
                                           Q(company__icontains=search) | \
                                           Q(email__icontains=search) | \
                                           Q(interest__icontains=search) | \
                                           Q(phone__icontains=search))


class ContactCreateView(CreateView):
    model = Contacts
    form_class = ContactViewForm
    success_url = reverse_lazy('contacts')


class ContactUpdateView(UpdateView):
    model = Contacts
    form_class = ContactViewForm
    template_name = 'contacts_update_form.html'
    success_url = reverse_lazy('contacts')


class ContactDeleteView(DeleteView):
    model = Contacts
    success_url = reverse_lazy('contacts')


class ContactDetailView(DetailView):
    model = Contacts


def export_json(request):
    contacts = Contacts.objects.all()
    data = serializers.serialize('python', contacts)

    d1 = []
    for dat in data:
        dat['fields'].update({'pk':dat['pk']})
        d1.append(dat['fields'])

    output = json.dumps(d1, indent=4)
    response = HttpResponse(output, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=export.json'
    return response


class FileUploadView(CreateView):
    form_class = FileUploadModelForm
    template_name = 'upload.html'
    success_url = reverse_lazy('contacts')


def import_json_site(request):
    r = requests.get("https://jsonplaceholder.typicode.com/users", verify=False)
    data = r.text
    data = json.loads(data)

    for d1 in data:
        out = {"name":d1['name'], "company":d1['company']['name'],
               "email":d1['email'], "phone":d1['phone'], "interest":""}
        form = ContactViewForm(out)

        if form.is_valid():
            form.save()

    return HttpResponseRedirect(reverse('contacts'))

