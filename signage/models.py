from __future__ import unicode_literals

from django.db.models import Model, BooleanField, DateTimeField, CharField, URLField, TextField, ForeignKey, PositiveIntegerField, ManyToManyField
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from adminsortable.models import SortableMixin, SortableForeignKey
from datetime import datetime

# Create your models here.

class Playlist(SortableMixin):
    name = CharField(max_length=140, default='Untitled', unique=True)
    # ordering field
    playlist_order = PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['playlist_order']
        verbose_name_plural = 'Playlists'

    def __unicode__(self):
        return self.name


class Asset(SortableMixin):
    name = CharField(max_length=140, default='Untitled Asset')
    kind = CharField(max_length=8, default='web', choices=(
        ('web', 'Web Page'),
        ('video', 'Video (MP4)'),
    ), verbose_name='Asset Type') 
    url = CharField(max_length=512, verbose_name='URL',validators=[URLValidator()])
    parameters = CharField(max_length=512,blank=True,null=True)
    duration = PositiveIntegerField(default=30, validators=[MaxValueValidator(1800),MinValueValidator(5),], verbose_name='Duration (s)')
    active = BooleanField(default=True)
    playlist = SortableForeignKey(Playlist)

    # ordering field
    asset_order = PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['asset_order']

    def __unicode__(self):
        return self.name

class Device(Model):
    device_id = CharField(max_length=128, default='00deadbeef42', unique=True, editable=False)
    mac_address = CharField(max_length=17, default='00:de:ad:be:ef:42', unique=True,editable=False, verbose_name='MAC Address')
    ip_address = CharField(max_length=45, default='127.0.0.1', editable=False, verbose_name='IP Address') # IPv6
    name = CharField(max_length=128,default='Unnamed Device', verbose_name='Device Name')
    active = BooleanField(default=False)
    playlist = ForeignKey(Playlist, blank=True, null=True)
    last_seen = DateTimeField(auto_now=True, editable=False, verbose_name='Last Seen')

    def __unicode__(self):
        return self.name


class Alert(Playlist):
    when = DateTimeField(verbose_name='Start At')
    active = BooleanField(default=True)
    devices = ManyToManyField(Device)
    shown_on = ManyToManyField(Device, editable=False, related_name="shown_on")

    class Meta:
        verbose_name_plural = 'Alerts'

    def __unicode__(self):
        return self.name

class PredefinedAsset(Model):
    name = CharField(max_length=140, default='Untitled Template')
    url = CharField(max_length=512, verbose_name='URL',validators=[URLValidator()])

    class Meta:
        verbose_name = 'Predefined Asset'
        verbose_name_plural = 'Predefined Assets'

    def __unicode__(self):
        return self.name