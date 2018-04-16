from .models import Contacts
from .serializers import ContactSerializer
from rest_framework import generics


class ContactList(generics.ListCreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer
