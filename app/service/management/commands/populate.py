from django.core.management.base import BaseCommand
from service.models import ServiceArea, ServiceType


class Command(BaseCommand):
    help = 'Populate ServiceArea model with data from a list of Florida counties'

    def handle(self, *args, **options):
        # You can read the data from a file, an API, or any other source
        # Here I use a hard-coded list for simplicity
        florida_counties = ["Alachua County",
                            "Baker County",
                            "Bay County",
                            "Bradford County",
                            "Brevard County",
                            "Broward County",
                            "Calhoun County",
                            "Charlotta Count",
                            "Citrus County",
                            "Clay County",
                            "Collier County",
                            "Columbia County",
                            "Dade County",
                            "De Soto County",
                            "Dixie County",
                            "Duval County",
                            "Escambia County",
                            "Flagler County",
                            "Franklin County",
                            "Gadsden County",
                            "Gilchrist Count",
                            "Glades County",
                            "Gulf County",
                            "Hamilton County",
                            "Hardee County",
                            "Hendry County",
                            "Hernando County",
                            "Highlands County",
                            "Hillsborough County",
                            "Holmes County",
                            "Indian River County",
                            "Jackson County",
                            "Jefferson County",
                            "Lafayette County",
                            "Lake County",
                            "Lee County",
                            "Leon County",
                            "Levy County",
                            "Liberty County",
                            "Madison County",
                            "Manatee County",
                            "Marion County",
                            "Martin County",]

        # Loop through the data and create or update the model instances
        for county in florida_counties:
            service_area, created = ServiceArea.objects.get_or_create(
                name=county)
            if created:
                service_area.description = f'Service area for {county}'
                service_area.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Created service area for {county}'))
            else:
                self.stdout.write(self.style.NOTICE(
                    f'Service area for {county} already exists'))

        rooftop_repair_services = [
            'Leaking roof repair',
            'Missing or damaged shingle replacement',
            'Sagging roof repair',
            'Flashing repair',
            'Valley repair',
            'Low slope or poor roof pitch repair',
            'Gutter and downspout repair',
            'Fascia and soffit repair',
            'Roof truss repair',
            'Garage roof repair',
        ]

        # Loop through the data and create the model instances
        for service in rooftop_repair_services:
            service_type, created = ServiceType.objects.get_or_create(name=service)
            if created:
                service_type.description = f'Service type for {service}'
                service_type.save()
                self.stdout.write(self.style.SUCCESS(f'Created service type for {service}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Service type for {service} already exists'))