from django import forms
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget

from calendar import monthrange

YEARS = [year for year in range(1850, 2013)]


class NewSelectDateWidget(SelectDateWidget):
    none_value = (0, 'unknown')


class AddPersonForm(ModelForm):
    years = [year for year in range(1850, 1950)]

    birth_earliest_date = forms.CharField(widget=NewSelectDateWidget(attrs={'class': 'input-small'}, years=years),
                                          required=False)
    birth_latest_date = forms.CharField(widget=NewSelectDateWidget(attrs={'class': 'input-small'}, years=years),
                                        required=False)
    birth_earliest_month_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    birth_earliest_day_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    birth_latest_month_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    birth_latest_day_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    death_earliest_date = forms.CharField(widget=NewSelectDateWidget(attrs={'class': 'input-small'}, years=years),
                                          required=False)
    death_latest_date = forms.CharField(widget=NewSelectDateWidget(attrs={'class': 'input-small'}, years=years),
                                        required=False)
    death_earliest_month_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    death_earliest_day_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    death_latest_month_known = forms.BooleanField(widget=forms.HiddenInput, required=False)
    death_latest_day_known = forms.BooleanField(widget=forms.HiddenInput, required=False)

    def clean_birth_earliest_date(self):
        return self.clean_date(self.cleaned_data['birth_earliest_date'], 'start')

    def clean_death_earliest_date(self):
        return self.clean_date(self.cleaned_data['death_earliest_date'], 'start')

    def clean_birth_latest_date(self):
        return self.clean_date(self.cleaned_data['birth_latest_date'], 'end')

    def clean_death_latest_date(self):
        return self.clean_date(self.cleaned_data['death_latest_date'], 'end')

    def clean_birth_earliest_month_known(self):
        return self.clean_month(self.cleaned_data['birth_earliest_date'], 'start')

    def clean_death_earliest_month_known(self):
        return self.clean_month(self.cleaned_data['death_earliest_date'], 'start')

    def clean_birth_earliest_day_known(self):
        return self.clean_day(self.cleaned_data['birth_earliest_date'], 'start')

    def clean_death_earliest_day_known(self):
        return self.clean_day(self.cleaned_data['death_earliest_date'], 'start')

    def clean_birth_latest_month_known(self):
        return self.clean_month(self.cleaned_data['birth_latest_date'], 'end')

    def clean_death_latest_month_known(self):
        return self.clean_month(self.cleaned_data['death_latest_date'], 'end')

    def clean_birth_latest_day_known(self):
        return self.clean_day(self.cleaned_data['birth_latest_date'], 'end')

    def clean_death_latest_day_known(self):
        return self.clean_day(self.cleaned_data['death_latest_date'], 'end')

    def clean_date(self, date, type):
        year, month, day = date.split('-')
        if int(month) == 0:
            if type == 'start':
                month = '0'
                day = '1'
            elif type == 'end':
                month = '12'
                day = '31'
        else:
            if int(day) == 0:
                if type == 'start':
                    day = '1'
                elif type == 'end':
                    day = monthrange(int(year), int(month))[1]
        return '%s-%s-%s' % (year, month, day)

    def clean_month(self, date, type):
        year, month, day = date.split('-')
        return False if int(month) == 0 else True

    def clean_day(self, date, type):
        year, month, day = date.split('-')
        return False if int(day) == 0 else True


class DateSelectMixin:

    def clean(self):
        cleaned_data = super().clean()
        all_date_fields = [f for f in self.fields if isinstance(self.fields[f].widget, NewSelectDateWidget)]
        for date_field in all_date_fields:
            date_data = cleaned_data[date_field].split('-')
            if len(date_data) != 3:
                self.add_error(date_field, "Invalid date.")
                continue
            try:
                year, month, day = (int(i) for i in date_data)
            except ValueError:
                self.add_error(date_field, "Invalid date.")
                continue
            if year == month == day == 0:
                cleaned_data[date_field] = None
                continue
            elif 0 in {year, month, day}:
                self.add_error(date_field, "Invalid date.")
            else:
                cleaned_data[date_field] = '%s-%s-%s' % (year, month, day)
        return cleaned_data


class ShortDateForm(DateSelectMixin, ModelForm):
    start_earliest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=YEARS
        ), required=False
    )
    end_earliest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=YEARS
        ), required=False
    )


class AddEventForm(DateSelectMixin, ModelForm):
    years = [year for year in range(1850, 2013)]
    # These are CharFields so they don't get validated as dates
    start_earliest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=years
        ), required=False)
    start_latest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=years
        ), required=False)
    end_earliest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=years
        ), required=False)
    end_latest_date = forms.CharField(
        widget=NewSelectDateWidget(
            attrs={'class': 'input-small'},
            years=years
        ), required=False)
