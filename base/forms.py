import datetime

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet, modelformset_factory
from .models import Client, Activity, Parcel, Quarter, Month, Category

class BaseMonthFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        for form in self.forms:
            form.save(commit=commit)
        return super(BaseMonthFormSet, self).save(commit=commit)


MonthFormSet = inlineformset_factory(
    Quarter,
    Month,
    fields=['total_price',],
    can_delete=False,
    min_num=3,
    max_num=3,
    formset=BaseMonthFormSet,
    widgets={
        'total_price': forms.NumberInput(
            attrs={
                'class':'form-control',
                'min':0,
            }
        )
    },
    labels={
        'total_price':''
    }
)

class BaseQuarterFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseQuarterFormSet, self).add_fields(form, index)

        form.nested = MonthFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f'quarter-{form.prefix}-{MonthFormSet.get_default_prefix()}',
        )

    def is_valid(self):
        valid = super(BaseQuarterFormSet, self).is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    valid = form.nested.is_valid() and valid
        return valid

    def save(self, commit=True):
        for form in self.forms:
            form.save(commit=commit)
            if hasattr(form, 'nested'):
                form.nested.save(commit=commit)
        return super(BaseQuarterFormSet, self).save(commit=commit)


QuarterFormSet = inlineformset_factory(
    Parcel,
    Quarter,
    formset=BaseQuarterFormSet,
    exclude='__all__',
    can_delete=False,
    min_num=4,
    max_num=4,
)

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['client', 'year']
        widgets = {
            'client' : forms.HiddenInput(),
            'year' : forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            )
        }
        labels = {
            'year':''
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['business_name',]
        widgets = {
            'business_name': forms.TextInput(
                attrs={
                    'placeholder':'Ragione Sociale',
                    'class':'form-control'
                }
            )
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name',]
        widgets = {
            'category_name': forms.TextInput(
                attrs={
                    'placeholder':'Nome categoria',
                    'class':'form-control'
                }
            )
        }

class ActivityForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        Category.objects.all(),
        widget=forms.Select(
            attrs={'class':'form-select'}
        )
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder':'dd-mm-yyyy', 'class':'form-control'}
        )
    )
    start_hour = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class':'form-control'}
        )
    )
    end_hour = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class':'form-control'}
        )
    )
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={'type': 'text', 'class':'form-control', 'cols':12, 'rows':1, 'placeholder':'Note'}
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        start = datetime.datetime.combine(cleaned_data['date'], cleaned_data['start_hour'])
        end = datetime.datetime.combine(cleaned_data['date'], cleaned_data['end_hour'])
        if end < start:
            raise forms.ValidationError({'start_hour':"L'ora di inizio deve essere precedente all'ora di fine"})

    class Meta:
        model = Activity
        fields = ['client', 'category', 'date', 'start_hour', 'end_hour', 'note']
        widgets = {'client': forms.HiddenInput()}
