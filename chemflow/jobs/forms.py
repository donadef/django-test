from django import forms

from .models import Job


SF_CHOICES_DOCK = (
    ('vina', 'Vina'),
    ('chemplp', 'ChemPLP'),
    ('plp95', 'plp95'),
    ('plp', 'plp'),
)


class JobDockForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"

        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control',
                                                   'required': 'required',
                                                   'placeholder': 'Project name'}),
            'protocol': forms.TextInput(attrs={'class': 'form-control',
                                               'required': 'required',
                                               'placeholder': 'Protocol name, one project may contain several protocols.',
                                               'oninput': 'update_job_name_with_protocol()'}),
            'job_name': forms.TextInput(attrs={'class': 'form-control',
                                               'required': 'required',
                                               'disabled': 'disabled',
                                               'placeholder': ' - '}),
            'sf': forms.Select(attrs={'class': 'form-control',
                                      'required': 'required'},
                               choices=SF_CHOICES_DOCK),

            'receptor_file': forms.FileInput(attrs={'class': 'form-control-file',
                                                    'required': 'required'}),
            'ligands_file': forms.FileInput(attrs={'class': 'form-control-file',
                                                   'required': 'required'}),

            'center_x': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'x'}),
            'center_y': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'y'}),
            'center_z': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'z'}),

            'radius': forms.NumberInput(attrs={'class': 'col-sm-4 w-25'}),

            'size_x': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'x'}),
            'size_y': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'y'}),
            'size_z': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'z'}),

        }


SF_CHOICES_SCORE = (
    ('vina', 'Vina'),
    ('chemplp', 'ChemPLP'),
    ('plp95', 'plp95'),
    ('plp', 'plp'),
    ('mmgbsa', 'MM-GBSA'),
    ('mmpbsa', 'MM-PBSA')
)


class JobScoreForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"

        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control',
                                                   'required': 'required',
                                                   'placeholder': 'Project name'}),
            'protocol': forms.TextInput(attrs={'class': 'form-control',
                                               'required': 'required',
                                               'placeholder': 'Protocol name, one project may contain several protocols.',
                                               'oninput': 'update_job_name_with_protocol()'}),
            'job_name': forms.TextInput(attrs={'class': 'form-control',
                                               'required': 'required',
                                               'disabled': 'disabled',
                                               'placeholder': ' - '}),
            'sf': forms.Select(attrs={'class': 'form-control',
                                      'required': 'required'},
                               choices=SF_CHOICES_SCORE),

            'receptor_file': forms.FileInput(attrs={'class': 'form-control-file',
                                                    'required': 'required'}),
            'ligands_file': forms.FileInput(attrs={'class': 'form-control-file',
                                                   'required': 'required'}),

            'center_x': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'x'}),
            'center_y': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'y'}),
            'center_z': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                                 'required': 'required',
                                                 'placeholder': 'z'}),

            'radius': forms.NumberInput(attrs={'class': 'col-sm-4 w-25'}),

            'size_x': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'x'}),
            'size_y': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'y'}),
            'size_z': forms.NumberInput(attrs={'class': 'col-sm-4 w-25',
                                               'required': 'required',
                                               'placeholder': 'z'}),

        }
