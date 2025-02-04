import datetime

from django import forms
from django.forms import ModelForm

from ckeditor.widgets import CKEditorWidget
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from app.people.models import *
from app.places.models import *
from app.sources.models import *
from app.generic.forms import AddEventForm, DateSelectMixin, ShortDateForm, NewSelectDateWidget


def get_range_upper_year():
    now = datetime.datetime.now().year
    return now + 1


YEARS = [year for year in range(1850, get_range_upper_year())]


class PeopleMultiChoice(ModelSelect2MultipleWidget):
    queryset = Person.objects
    search_fields = ['family_name__istartswith', ]

    def clean(self):
        cleaned_data = super(AddPersonForm, self).clean()
        birth_earliest_date = cleaned_data['birth_earliest_date']
        birth_latest_date = cleaned_data['birth_latest_date']
        cleaned_data['birth_earliest_month_known'] = self.clean_month(birth_earliest_date, 'start')
        cleaned_data['birth_earliest_day_known'] = self.clean_day(birth_earliest_date, 'start')
        cleaned_data['birth_latest_month_known'] = self.clean_month(birth_latest_date, 'end')
        cleaned_data['birth_latest_day_known'] = self.clean_day(birth_latest_date, 'end')
        cleaned_data['birth_earliest_date'] = self.clean_date(birth_earliest_date, 'start')
        cleaned_data['birth_latest_date'] = self.clean_date(birth_latest_date, 'end')
        death_earliest_date = cleaned_data['death_earliest_date']
        death_latest_date = cleaned_data['death_latest_date']
        cleaned_data['death_earliest_month_known'] = self.clean_month(death_earliest_date, 'start')
        cleaned_data['death_earliest_day_known'] = self.clean_day(death_earliest_date, 'start')
        cleaned_data['death_latest_month_known'] = self.clean_month(death_latest_date, 'end')
        cleaned_data['death_latest_day_known'] = self.clean_day(death_latest_date, 'end')
        cleaned_data['death_earliest_date'] = self.clean_date(death_earliest_date, 'start')
        cleaned_data['death_latest_date'] = self.clean_date(death_latest_date, 'end')
        return cleaned_data


class PersonChoice(ModelSelect2Widget):
    queryset = Person.objects
    search_fields = ['family_name__istartswith', ]


class PlaceChoice(ModelSelect2Widget):
    queryset = Place.objects
    search_fields = ['display_name__istartswith', 'place_name__istartswith']


class OrganisationChoice(ModelSelect2Widget):
    queryset = Organisation.objects
    search_fields = ['display_name__istartswith', 'name__istartswith']


class LifeEventChoice(ModelSelect2Widget):
    queryset = LifeEvent.objects


class SourcesMultiChoice(ModelSelect2MultipleWidget):
    queryset = Source.objects
    search_fields = ['title__icontains', ]


class EventLocationsMultiChoice(ModelSelect2MultipleWidget):
    queryset = EventLocation.objects
    search_fields = ['label__icontains', ]


class AddPersonForm(DateSelectMixin, ModelForm):
    # These are CharFields so they don't get validated as dates
    related_person = forms.ModelChoiceField(
        queryset=PersonAssociatedPerson.objects.select_related('person', 'associated_person', 'association'),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    source = forms.ModelChoiceField(
        queryset=Source.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    creator_type = forms.CharField(required=False, widget=forms.HiddenInput())
    birth_earliest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)
    birth_latest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)
    death_earliest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)
    death_latest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)

    def clean(self):
        cleaned_data = super(AddPersonForm, self).clean()
        birth_earliest_date = cleaned_data['birth_earliest_date']
        birth_latest_date = cleaned_data['birth_latest_date']
        cleaned_data['birth_earliest_month_known'] = self.clean_month(birth_earliest_date, 'start')
        cleaned_data['birth_earliest_day_known'] = self.clean_day(birth_earliest_date, 'start')
        cleaned_data['birth_latest_month_known'] = self.clean_month(birth_latest_date, 'end')
        cleaned_data['birth_latest_day_known'] = self.clean_day(birth_latest_date, 'end')
        cleaned_data['birth_earliest_date'] = self.clean_date(birth_earliest_date, 'start')
        cleaned_data['birth_latest_date'] = self.clean_date(birth_latest_date, 'end')
        death_earliest_date = cleaned_data['death_earliest_date']
        death_latest_date = cleaned_data['death_latest_date']
        cleaned_data['death_earliest_month_known'] = self.clean_month(death_earliest_date, 'start')
        cleaned_data['death_earliest_day_known'] = self.clean_day(death_earliest_date, 'start')
        cleaned_data['death_latest_month_known'] = self.clean_month(death_latest_date, 'end')
        cleaned_data['death_latest_day_known'] = self.clean_day(death_latest_date, 'end')
        cleaned_data['death_earliest_date'] = self.clean_date(death_earliest_date, 'start')
        cleaned_data['death_latest_date'] = self.clean_date(death_latest_date, 'end')
        return cleaned_data

    class Meta:
        model = Person
        exclude = ('added_by', 'status')
        widgets = {
            # 'birth_earliest_month_known': forms.HiddenInput,
            # 'birth_earliest_day_known': forms.HiddenInput,
            # 'birth_latest_month_known': forms.HiddenInput,
            # 'birth_latest_day_known': forms.HiddenInput,
            # 'death_earliest_month_known': forms.HiddenInput,
            # 'death_earliest_day_known': forms.HiddenInput,
            # 'death_latest_month_known': forms.HiddenInput,
            # 'death_latest_day_known': forms.HiddenInput,
            'biography': CKEditorWidget(attrs={'class': 'input-xlarge'}),
            'notes': CKEditorWidget(attrs={'class': 'input-xlarge'}),
            'mosman_connection': forms.Textarea(attrs={
                'class': 'input-xlarge',
                'rows': '4'
            })
        }


class UpdatePersonForm(AddPersonForm):
    pass


class ApprovePersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('status',)


class AddAltNameForm(ModelForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    sources = SourcesMultiChoice(required=False)

    class Meta:
        model = AlternativePersonName
        exclude = ('added_by',)


class AddLifeEventForm(AddEventForm):
    person = PersonChoice()
    sources = SourcesMultiChoice(required=False)

    # event_type = forms.ModelChoiceField(queryset=LifeEventType.objects.all(), required=False)

    class Meta:
        model = LifeEvent
        exclude = ('added_by',)
        widgets = {
            # 'start_earliest_month': forms.HiddenInput,
            # 'start_earliest_day': forms.HiddenInput,
            # 'start_latest_month': forms.HiddenInput,
            # 'start_latest_day': forms.HiddenInput,
            # 'end_earliest_month': forms.HiddenInput,
            # 'end_earliest_day': forms.HiddenInput,
            # 'end_latest_month': forms.HiddenInput,
            # 'end_latest_day': forms.HiddenInput,
            'description': forms.Textarea(attrs={
                'class': 'input-large',
                'rows': '4'})
        }


class AddEventLocationForm(forms.ModelForm):
    lifeevent = LifeEventChoice()
    location = PlaceChoice(required=False)

    class Meta:
        model = EventLocation
        fields = ('lifeevent', 'location')


class AddBirthForm(AddEventForm):
    person = PersonChoice()
    location = PlaceChoice(required=False)
    sources = SourcesMultiChoice(required=False)

    class Meta:
        model = Birth
        exclude = ('added_by',)


class AddDeathForm(AddEventForm):
    person = PersonChoice()
    location = PlaceChoice(required=False)
    sources = SourcesMultiChoice(required=False)

    class Meta:
        model = Death
        exclude = ('added_by',)


class AddRankForm(ShortDateForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    sources = SourcesMultiChoice(required=False)

    class Meta:
        model = Rank
        exclude = ('added_by',)


class AddServiceNumberForm(ModelForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    sources = SourcesMultiChoice(required=False)

    class Meta:
        model = ServiceNumber
        exclude = ('added_by',)


class AddOrganisationForm(ShortDateForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    person_organisation = forms.ModelChoiceField(
        queryset=PersonAssociatedOrganisation.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Organisation
        exclude = ('added_by',)


class AddAssociatedPersonForm(ShortDateForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.only('id', 'family_name', 'other_names', 'name_suffix', 'display_name')
    )
    associated_person = forms.ModelChoiceField(
        queryset=Person.objects.only('id', 'family_name', 'other_names', 'name_suffix', 'display_name'), required=False)
    association = forms.ModelChoiceField(queryset=PersonAssociation.objects.only('id', 'label'))

    class Meta:
        model = PersonAssociatedPerson
        exclude = ('added_by',)


class AddAssociatedOrganisationForm(DateSelectMixin, ModelForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    start_earliest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)
    end_earliest_date = forms.CharField(widget=NewSelectDateWidget(
        attrs={'class': 'input-small'},
        years=YEARS), required=False)
    organisation = OrganisationChoice()
    sources = SourcesMultiChoice(required=False)

    def clean(self):
        cleaned_data = super(AddAssociatedOrganisationForm, self).clean()
        start_earliest_date = cleaned_data['start_earliest_date']
        cleaned_data['start_earliest_month'] = self.clean_month(start_earliest_date, 'start')
        cleaned_data['start_earliest_day'] = self.clean_day(start_earliest_date, 'start')
        cleaned_data['start_earliest_date'] = self.clean_date(start_earliest_date, 'start')
        end_earliest_date = cleaned_data['end_earliest_date']
        cleaned_data['end_earliest_month'] = self.clean_month(end_earliest_date, 'start')
        cleaned_data['end_earliest_day'] = self.clean_day(end_earliest_date, 'start')
        cleaned_data['end_earliest_date'] = self.clean_date(end_earliest_date, 'start')
        return cleaned_data

    class Meta:
        model = PersonAssociatedOrganisation
        exclude = ('added_by',)
        widgets = {
            'start_earliest_month': forms.HiddenInput,
            'start_earliest_day': forms.HiddenInput,
            'end_earliest_month': forms.HiddenInput,
            'end_earliest_day': forms.HiddenInput,
        }


class AddPersonAddressForm(ShortDateForm):
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    sources = SourcesMultiChoice(required=False)
    address = forms.ModelChoiceField(
        queryset=Address.objects.select_related('mosman_street', 'place')
    )

    class Meta:
        model = PersonAddress
        exclude = ('added_by',)


class PersonMergeForm(forms.Form):
    merge_record = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    master_record = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=forms.Select()
    )


class OrganisationMergeForm(forms.Form):
    merge_record = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        widget=forms.Select(attrs={'readonly': 'readonly'})
    )
    master_record = OrganisationChoice()
