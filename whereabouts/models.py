from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class SocialNetwork(models.Model):
    name = models.CharField(max_length=50, unique=True)
    site_url = models.URLField(verify_exists=False)
    icon = models.ImageField(
        upload_to='whereabouts/sn_icons/', 
        max_length=200, 
        null=True, 
        blank=True
    )
    profile_template = models.CharField(
        max_length=255, 
        blank=True,
        help_text= """
            Enter URL template with {profileid} as a placeholder for the user's
            unique id on the network. Leave blank for default of http://domain/{profileid}            
        """
    )
    
    class Meta:
        ordering = ('name',)
        
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.profile_template:
            self.profile_template = '%s{profileid}' % self.site_url
        super(SocialNetwork, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return self.site_url
    
    def get_icon_image_source(self):
        return '<img src="%s%s" />' % (settings.MEDIA_URL, self.icon,)
    get_icon_image_source.allow_tags = True
    
class SocialNetworkProfile(models.Model):
    network = models.ForeignKey(SocialNetwork)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    profile_id = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('network',)
        
    def __unicode__(self):
        return "%s's (%s) profile on %s" % (self.content_object, 
                                            self.content_type.name, 
                                            self.network.name)
        
    def get_absolute_url(self):
        return self.network.profile_template.replace('{profileid}', self.profile_id)