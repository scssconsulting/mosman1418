# Generated by Django 2.2.13 on 2021-05-21 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorials', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='alternativepersonname',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='birth',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='death',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='lifeevent',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='personaddress',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='personassociatedorganisation',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='personassociatedperson',
        #     name='sources',
        # ),
        # migrations.RemoveField(
        #     model_name='rank',
        #     name='sources',
        # ),
        migrations.RemoveField(
            model_name='servicenumber',
            name='sources',
        ),
        migrations.AddField(
            model_name='alternativepersonname',
            name='memorials',
            field=models.ManyToManyField(blank=True, to='memorials.Memorial'),
        ),
        migrations.AddField(
            model_name='death',
            name='memorials',
            field=models.ManyToManyField(blank=True, to='memorials.Memorial'),
        ),
        migrations.AddField(
            model_name='lifeevent',
            name='memorials',
            field=models.ManyToManyField(blank=True, to='memorials.Memorial'),
        ),
        migrations.AddField(
            model_name='personassociatedorganisation',
            name='memorials',
            field=models.ManyToManyField(blank=True, to='memorials.Memorial'),
        ),
        migrations.AddField(
            model_name='rank',
            name='memorials',
            field=models.ManyToManyField(blank=True, to='memorials.Memorial'),
        ),
        migrations.AlterField(
            model_name='lifeevent',
            name='locations',
            field=models.ManyToManyField(blank=True, through='people.EventLocation', to='places.Place'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='associated_sources',
            field=models.ManyToManyField(blank=True, through='people.OrganisationAssociatedSource', to='sources.Source'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='stories',
            field=models.ManyToManyField(blank=True, to='sources.Story'),
        ),
        migrations.AlterField(
            model_name='person',
            name='addresses',
            field=models.ManyToManyField(blank=True, through='people.PersonAddress', to='places.Address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_events',
            field=models.ManyToManyField(blank=True, through='people.PersonAssociatedEvent', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_objects',
            field=models.ManyToManyField(blank=True, through='people.PersonAssociatedObject', to='objects.Object'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_organisations',
            field=models.ManyToManyField(blank=True, through='people.PersonAssociatedOrganisation', to='people.Organisation'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_people',
            field=models.ManyToManyField(blank=True, related_name='related_people', through='people.PersonAssociatedPerson', to='people.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_places',
            field=models.ManyToManyField(blank=True, through='people.PersonAssociatedPlace', to='places.Place'),
        ),
        migrations.AlterField(
            model_name='person',
            name='associated_sources',
            field=models.ManyToManyField(blank=True, through='people.PersonAssociatedSource', to='sources.Source'),
        ),
        migrations.AlterField(
            model_name='person',
            name='images',
            field=models.ManyToManyField(blank=True, to='people.PeopleImage'),
        ),
        migrations.AlterField(
            model_name='person',
            name='stories',
            field=models.ManyToManyField(blank=True, to='sources.Story'),
        ),
    ]
