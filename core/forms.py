from django import forms
from .models import Photo, Video, KeyInfo, OrganizationContent, Notice, Career,Governance
from ckeditor.widgets import CKEditorWidget
from django.utils import timezone

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'id': 'name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'id': 'email',
        })
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
            'id': 'subject',
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Leave a message here',
            'id': 'message',
            'style': 'height: 150px;',
        })
    )



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_url']   



class KeyInfoForm(forms.ModelForm):
    class Meta:
        model = KeyInfo
        fields = ['key_strategy', 'key_achievement', 'why_hands_nepal'] 


# forms.py
class GovernanceForm(forms.ModelForm):
    class Meta:
        model = Governance
        fields = ['photo', 'name', 'position', 'expertise', 'phone', 'email']


class OrganizationContentForm(forms.ModelForm):
    class Meta:
        model = OrganizationContent
        fields = '__all__'
        widgets = {
            'mission': CKEditorWidget(),
            'vision': CKEditorWidget(),
            'goal': CKEditorWidget(),
            'objective': CKEditorWidget(),
            'value': CKEditorWidget(),
            'geo_area': CKEditorWidget(),
            'theme_area': CKEditorWidget(),
        }        

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'image', 'attachment', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'attachment': 'Upload a file (PDF, DOC, etc.) related to this notice (optional)',
            'is_active': 'Uncheck to hide this notice from the website',
        }


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['title', 'description', 'opening_date', 'closing_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter job description and requirements'
            }),
            'opening_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'closing_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        help_texts = {
            'closing_date': 'Last date to apply for this position',
        }

    def clean(self):
        cleaned_data = super().clean()
        opening_date = cleaned_data.get('opening_date')
        closing_date = cleaned_data.get('closing_date')
        
        if opening_date and closing_date:
            if opening_date > closing_date:
                raise forms.ValidationError("Closing date must be after opening date.")
            if closing_date < timezone.now().date():
                raise forms.ValidationError("Closing date must be in the future.")
        
        return cleaned_data


class CareerApplicationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address',
            'required': 'required'
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number',
            'required': 'required'
        })
    )
    resume = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx',
            'required': 'required'
        }),
        help_text='Upload your resume (PDF or DOCX, max 5MB)'
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Any additional information you would like to share'
        })
    )

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            file_extension = resume.name.split('.')[-1].lower()
            if file_extension not in ['pdf', 'doc', 'docx']:
                raise forms.ValidationError('Only PDF and Word documents are allowed.')
            if resume.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('File size should not exceed 5MB.')
        return resume


# class CareerForm(forms.ModelForm):
#     class Meta:
#         model = Career
#         fields = ['title', 'description', 'file']
#         widgets = {
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#         help_texts = {
#             'file': 'Upload a file (PDF, DOC, etc.) related to this career (optional)',
#             'description': 'Enter a description for this career (optional)',
#             'title': 'Enter a title for this career (optional)',
#         }
    