from django import forms

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    

class RemoveDuples(forms.Form):
    pass

class ProcessFileForm(forms.Form):
    """
    class Meta:
        fields = ['placeholder']
    
    #text = forms.CharField(widget=forms.Textarea)
    """
    
    
    def __init__(self, dynamic_field_names, *args, **kwargs):
        # number of parameters in conf from xlsx_parser.yaml to skip 
        conf_to_skip = ('categories', 'test_tab')
        #conf_to_skip = 2
        
        super(ProcessFileForm, self).__init__(*args, **kwargs)

        #for field_name in dynamic_field_names:
            # self.fields[field_name] = forms.CharField(max_length=32)    # creates a dynamic field
            
        self.fields['xlsx_tabs'] = forms.ChoiceField(
        #xlsx_tabs = forms.ChoiceField(
            choices=[(idx, str(field_name)) for idx, field_name in enumerate(dynamic_field_names[1])]
        )
        
        conf_fields = dynamic_field_names[0]
        #print(conf_fields)
        if len(conf_fields) > 0:
            # skip parameters from the beginng
            # conf_fields = conf_fields[conf_to_skip:]
            
            self.fields['conf'] = forms.ChoiceField(
            #xlsx_tabs = forms.ChoiceField(
                choices=[(idx, str(field_name)) for idx, field_name in enumerate(conf_fields) if field_name not in conf_to_skip]
            )