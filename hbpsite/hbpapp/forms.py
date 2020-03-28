from django import forms

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    

class ProcessFileForm(forms.Form):
    
    class Meta:
        fields = ['placeholder']
    
    #text = forms.CharField(widget=forms.Textarea)
    """
    def __init__(self, dynamic_field_names, *args, **kwargs):
        super(ProcessFileForm, self).__init__(*args, **kwargs)

        for field_name in dynamic_field_names:
            self.fields[field_name] = forms.CharField(max_legth=32)    # creates a dynamic field
    """
