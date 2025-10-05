from django.core.management.base import BaseCommand
import csv
import os
from django.conf import settings
from api.models import MarsRegion, MarsCrop


class Command(BaseCommand):
    help = 'Load Mars regions and crops data from CSV files'

    def handle(self, *args, **options):
        # Load Mars regions
        regions_file = os.path.join(settings.BASE_DIR, 'data', 'mars_regions.csv')
        if os.path.exists(regions_file):
            self.stdout.write('Loading Mars regions...')
            with open(regions_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    MarsRegion.objects.get_or_create(
                        region=row['Region'],
                        defaults={
                            'latitude_deg': row.get('Latitude_deg', ''),
                            'longitude_deg': row.get('Longitude_deg', ''),
                            'elevation_m': row.get('Elevation_m', ''),
                            'perchlorate_wt_pct': row.get('Perchlorate_wt_pct', ''),
                            'water_release_wt_pct': row.get('Water_release_wt_pct', ''),
                            'ph': row.get('pH', ''),
                            'major_minerals': row.get('Major_minerals', ''),
                            'terrain_type': row.get('Terrain_type', ''),
                            'notes': row.get('Notes', ''),
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Mars regions loaded successfully'))

        # Load Mars crops
        crops_file = os.path.join(settings.BASE_DIR, 'data', 'mars_crops_enhanced.csv')
        if os.path.exists(crops_file):
            self.stdout.write('Loading Mars crops...')
            with open(crops_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    MarsCrop.objects.get_or_create(
                        crop=row['Crop'],
                        defaults={
                            'germination_on_mars_simulant': row.get('Germination_on_MarsSimulant', ''),
                            'biomass': row.get('Biomass', ''),
                            'flowered_seed': row.get('Flowered/Seed', ''),
                            'notes': row.get('Notes', ''),
                            'preferred_ph_range': row.get('Preferred_pH_range', ''),
                            'terrain_soil_texture': row.get('Terrain_Soil_texture', ''),
                            'temperature_range_c': row.get('Temperature_range_C', ''),
                            'humidity_rh_range': row.get('Humidity_RH_range', ''),
                            'moisture_regime': row.get('Moisture_regime', ''),
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Mars crops loaded successfully'))

        self.stdout.write(self.style.SUCCESS('Data loading completed!'))
