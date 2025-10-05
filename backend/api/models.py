from django.db import models


class MarsSite(models.Model):
    """Model for Mars exploration sites."""
    
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    
    # Simulator parameters as JSON field
    simulator_parameters = models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mars_sites'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MarsRegion(models.Model):
    """Model for Mars regions data."""
    
    region = models.CharField(max_length=200)
    latitude_deg = models.CharField(max_length=50)
    longitude_deg = models.CharField(max_length=50)
    elevation_m = models.CharField(max_length=50, blank=True, null=True)
    perchlorate_wt_pct = models.CharField(max_length=50, blank=True, null=True)
    water_release_wt_pct = models.CharField(max_length=50, blank=True, null=True)
    ph = models.CharField(max_length=50, blank=True, null=True)
    major_minerals = models.TextField(blank=True, null=True)
    terrain_type = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mars_regions'
        ordering = ['region']
    
    def __str__(self):
        return self.region


class MarsCrop(models.Model):
    """Model for Mars crops data."""
    
    crop = models.CharField(max_length=200)
    germination_on_mars_simulant = models.CharField(max_length=50)
    biomass = models.CharField(max_length=100)
    flowered_seed = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    preferred_ph_range = models.CharField(max_length=100, blank=True, null=True)
    terrain_soil_texture = models.TextField(blank=True, null=True)
    temperature_range_c = models.CharField(max_length=100, blank=True, null=True)
    humidity_rh_range = models.CharField(max_length=100, blank=True, null=True)
    moisture_regime = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mars_crops'
        ordering = ['crop']
    
    def __str__(self):
        return self.crop
