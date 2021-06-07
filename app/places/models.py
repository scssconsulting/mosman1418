from django.db import models
from django.urls import reverse

from app.generic.models import Place as GenericPlace, StandardMetadata


class Place(GenericPlace):
    place_name = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    geonames_id = models.IntegerField(blank=True, null=True)
    sources = models.ManyToManyField('sources.Source', blank=True)
    merged_into = models.ForeignKey('places.Place', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if not self.place_name:
            summary = self.display_name if self.display_name else '{}{}'.format(
                ', {}'.format(self.state) if self.state else '',
                ', {}'.format(self.country) if self.country else ''
            )
        else:
            summary = '{}{}{}'.format(
                self.place_name,
                ', {}'.format(self.state) if self.state else '',
                ', {}'.format(self.country) if self.country else ''
            )
        return summary

    def get_absolute_url(self):
        return reverse('place-view', args=[self.id])

    def burial_places(self):
        people = list(set(self.burial_place.values_list('person__family_name', 'person__other_names', 'person')))
        return people

    def death_places(self):
        people = list(set(self.death_set.values_list('person__family_name', 'person__other_names', 'person')))
        return people

    def birth_places(self):
        people = list(set(self.birth_set.values_list('person__family_name', 'person__other_names', 'person')))
        return people

    class Meta:
        ordering = ['place_name']
        permissions = [('merge_place', 'Merge place')]


class Address(StandardMetadata):
    building_name = models.CharField(max_length=250, blank=True)
    street_name = models.CharField(max_length=250, blank=True)
    street_number = models.CharField(max_length=250, blank=True)
    mosman_street = models.ForeignKey('places.MosmanStreet', on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey('places.Place', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.mosman_street and self.mosman_street.street_name:
            street = self.mosman_street.street_name
        elif self.street_name:
            street = self.street_name
        else:
            street = ''
        building_street = '{building}{number}{street}'.format(
            building='{}, '.format(self.building_name).strip(',') if self.building_name else '',
            number='{} '.format(self.street_number) if self.street_number else '',
            street='{}'.format(street if street else '')
        ).strip().strip(',')
        return '{}, {}'.format(
            building_street,
            self.place or ''
        ).strip(',')

    class Meta:
        ordering = ['street_name', 'mosman_street__street_name', 'street_number']

    def get_absolute_url(self):
        return reverse('address-view', args=[self.id])


class MosmanStreet(models.Model):
    street_name = models.CharField(max_length=250, blank=True)
    bounding_box = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.street_name

    def get_absolute_url(self):
        return reverse('mosmanstreet-view', args=[self.id])
