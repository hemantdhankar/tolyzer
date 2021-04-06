from django import forms
from .validators import validate_file_extension
class uploadFile(forms.Form):
    network = forms.FileField(validators=[validate_file_extension])
    