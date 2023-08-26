from django.core.management.base import BaseCommand
from service.models import ServiceArea, ServiceType, Testimonials


class Command(BaseCommand):
    help = 'Populate ServiceArea model with data from a list of Florida counties'

    def handle(self, *args, **options):
        # You can read the data from a file, an API, or any other source
        # Here I use a hard-coded list for simplicity
        florida_counties = ["Alachua",
                                "Baker",
                                "Bay",
                                "Bradford",
                                "Brevard",
                                "Broward",
                                "Calhoun",
                                "Charlotte",
                                "Citrus",
                                "Clay",
                                "Collier",
                                "Columbia",
                                "DeSoto",
                                "Dixie",
                                "Duval",
                                "Escambia",
                                "Flagler",
                                "Franklin",
                                "Gadsden",
                                "Gilchrist",
                                "Glades",
                                "Gulf",
                                "Hamilton",
                                "Hardee",
                                "Hendry",
                                "Hernando",
                                "Highlands",
                                "Hillsboroug",
                                "Holmes",
                                "Indian Rive",
                                "Jackson",
                                "Jefferson",
                                "Lafayette",
                                "Lake",
                                "Lee",
                                "Leon",
                                "Levy",
                                "Liberty",
                                "Madison",
                                'Manatee',
                                "Marion",
                                "Martin",
                                "Miami-Dade",
                                "Monroe",
                                "Nassau",
                                "Okaloosa",
                                'Okeechobee',
                                "Orange",
                                "Osceola",
                                "Palm Beach",
                                "Pasco",
                                "Pinellas",
                                "Polk",
                                "Putnam",
                                "Santa Rosa",
                                "Sarasota",
                                "Seminole",
                               "St. Johns",
                                "St. Lucie",
                                "Sumter",
                                "Suwannee",
                                "Taylor",
                                "Union",
                                "Volusia",
                                "Wakulla",
                                "Walton",
                                "Washington"]

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
                
                
        Testimoniales = [
            {"name": "John Doe",
             "type_of_client":"Client",
             "message": "\"Florida Roof Marketplace provided excellent service. Their team of professionals repaired my leaking roof efficiently and at a reasonable cost. Highly recommended!\""},
            {"name": "Jane Smith",
             "type_of_client":"Homeowner",
             "message": "\"I had missing shingles on my roof, and Florida Roof Marketplace connected me with a skilled roofer who did a fantastic job replacing them. The process was seamless, and I'm very satisfied with the results.\""},
            {"name": "David Wilson",
             "type_of_client":"Business Owner",
             "message": "\"I contacted Florida Roof Marketplace for a sagging roof issue, and they quickly matched me with an experienced contractor. The team worked diligently and resolved the problem professionally. Thank you!\""},
            {"name": "Linda Thompson",
             "type_of_client":"Property Manager",
             "message": "\"Florida Roof Marketplace is a reliable platform for finding roof repair services. They helped me address flashing issues on multiple properties, and the service providers they recommended delivered exceptional results.\""},
        ]
        
        for t in Testimoniales:
            testimo, created = Testimonials.objects.get_or_create(name=t['name'])
            if created:
                testimo.type_of_client = t['type_of_client']
                testimo.message = t['message']
                testimo.save()
                self.stdout.write(self.style.SUCCESS(f'Created  {t["name"]}'))
            else:
                self.stdout.write(self.style.NOTICE(f'{t["name"]} already exists'))
                