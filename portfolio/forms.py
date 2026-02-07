

# from django import forms
# from chat.models import ChatMessage

# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['name', 'email', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows':4, 'placeholder':'Your message...'})
#         }


from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

