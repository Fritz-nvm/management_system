from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import UserRole, Branch, Asset
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Populate sample data for the Hospital Asset Management system"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        branches_data = [
            {
                "name": "Yaoundé Central Hospital",
                "code": "YAO-CH-001",
                "city": "Yaoundé",
                "region": "Centre",
                "manager_name": "Dr. Samuel Fokoua",
                "manager_phone": "+237 699 123 456",
            },
            {
                "name": "Douala General Hospital",
                "code": "DLA-GH-002",
                "city": "Douala",
                "region": "Littoral",
                "manager_name": "Dr. Alice Mbelle",
                "manager_phone": "+237 699 234 567",
            },
            {
                "name": "Bamenda Regional Hospital",
                "code": "BAM-RH-003",
                "city": "Bamenda",
                "region": "North-West",
                "manager_name": "Dr. Joseph Nkosi",
                "manager_phone": "+237 699 345 678",
            },
        ]

        branches = []
        for data in branches_data:
            branch, _ = Branch.objects.get_or_create(code=data["code"], defaults=data)
            branches.append(branch)
            self.stdout.write(self.style.SUCCESS(f"✓ Created branch: {branch.name}"))

        users_data = [
            {
                "username": "admin@hospital.cm",
                "email": "admin@hospital.cm",
                "password": "Admin123!",
                "role": "super_admin",
                "branch": None,
            },
            {
                "username": "manager@hospital.cm",
                "email": "manager@hospital.cm",
                "password": "Manager123!",
                "role": "branch_manager",
                "branch": branches[0],
            },
            {
                "username": "officer@hospital.cm",
                "email": "officer@hospital.cm",
                "password": "Officer123!",
                "role": "inventory_officer",
                "branch": branches[0],
            },
        ]

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "is_superuser": data["role"] == "super_admin",
                    "is_staff": data["role"] == "super_admin",
                },
            )

            if created:
                user.set_password(data["password"])
                user.save()

            role, _ = UserRole.objects.get_or_create(
                user=user, defaults={"role": data["role"], "branch": data["branch"]}
            )

            self.stdout.write(
                self.style.SUCCESS(f'✓ Created user: {user.username} ({data["role"]})')
            )

        base_date = datetime.now() - timedelta(days=60)
        assets_data = [
            {
                "name": "Ultrasound Machine",
                "category": "medical_equipment",
                "brand": "GE",
                "model": "Logiq E9",
                "serial_number": "US-001-GE",
                "branch": branches[0],
                "department": "radiology",
                "purchase_date": base_date + timedelta(days=30),
                "purchase_cost": 45000000,
                "supplier_name": "MediTech Solutions",
                "status": "in_use",
                "condition": "excellent",
                "custodian_name": "Dr. Yannick Mensah",
                "custodian_phone": "+237 699 111 111",
            },
            {
                "name": "X-Ray Machine",
                "category": "medical_equipment",
                "brand": "Siemens",
                "model": "AXIOM",
                "serial_number": "XR-001-SIE",
                "branch": branches[0],
                "department": "radiology",
                "purchase_date": base_date + timedelta(days=15),
                "purchase_cost": 125000000,
                "supplier_name": "Medical Imaging Ltd",
                "status": "in_use",
                "condition": "good",
                "custodian_name": "Dr. Marc Anye",
                "custodian_phone": "+237 699 111 222",
            },
            {
                "name": "Patient Monitor",
                "category": "medical_equipment",
                "brand": "Philips",
                "model": "IntelliVue",
                "serial_number": "PM-001-PHI",
                "branch": branches[1],
                "department": "emergency",
                "purchase_date": base_date + timedelta(days=45),
                "purchase_cost": 8500000,
                "supplier_name": "Healthcare Supplies Co",
                "status": "available",
                "condition": "excellent",
                "custodian_name": "Nurse Amandine Koa",
                "custodian_phone": "+237 699 222 333",
            },
            {
                "name": "Toyota Ambulance",
                "category": "vehicle",
                "brand": "Toyota",
                "model": "Hiace",
                "serial_number": "TYT-AMB-001",
                "branch": branches[0],
                "department": "emergency",
                "purchase_date": base_date + timedelta(days=60),
                "purchase_cost": 35000000,
                "supplier_name": "Toyota Motors Cameroon",
                "status": "in_use",
                "condition": "good",
                "custodian_name": "Driver Jean Claude",
                "custodian_phone": "+237 699 333 444",
            },
            {
                "name": "Nissan Ambulance",
                "category": "vehicle",
                "brand": "Nissan",
                "model": "NV200",
                "serial_number": "NIS-AMB-001",
                "branch": branches[1],
                "department": "emergency",
                "purchase_date": base_date + timedelta(days=50),
                "purchase_cost": 28000000,
                "supplier_name": "Nissan Distributors",
                "status": "maintenance",
                "condition": "fair",
                "custodian_name": "Driver Franck Tala",
                "custodian_phone": "+237 699 444 555",
            },
            {
                "name": "Cummins Generator",
                "category": "generator",
                "brand": "Cummins",
                "model": "C250",
                "serial_number": "CUM-GEN-001",
                "branch": branches[2],
                "department": "maintenance",
                "purchase_date": base_date + timedelta(days=40),
                "purchase_cost": 18000000,
                "supplier_name": "Power Solutions Ltd",
                "status": "in_use",
                "condition": "good",
                "custodian_name": "Engineer Emmanuel Che",
                "custodian_phone": "+237 699 555 666",
            },
            {
                "name": "Perkins Generator",
                "category": "generator",
                "brand": "Perkins",
                "model": "GP75",
                "serial_number": "PER-GEN-001",
                "branch": branches[1],
                "department": "maintenance",
                "purchase_date": base_date + timedelta(days=35),
                "purchase_cost": 22000000,
                "supplier_name": "Power Solutions Ltd",
                "status": "available",
                "condition": "excellent",
                "custodian_name": "Technician Peter Molua",
                "custodian_phone": "+237 699 666 777",
            },
            {
                "name": "Hospital Beds",
                "category": "furniture",
                "brand": "Standard",
                "model": "Adjustable",
                "serial_number": "HB-BEDS-100",
                "branch": branches[0],
                "department": "surgery",
                "purchase_date": base_date + timedelta(days=25),
                "purchase_cost": 5500000,
                "supplier_name": "Furniture Suppliers",
                "status": "in_use",
                "condition": "good",
                "custodian_name": "Mr. Henry Teke",
                "custodian_phone": "+237 699 777 888",
            },
            {
                "name": "Dell Computer",
                "category": "computer",
                "brand": "Dell",
                "model": "OptiPlex 7090",
                "serial_number": "DEL-COMP-001",
                "branch": branches[0],
                "department": "administration",
                "purchase_date": base_date + timedelta(days=20),
                "purchase_cost": 1200000,
                "supplier_name": "Tech Store",
                "status": "in_use",
                "condition": "excellent",
                "custodian_name": "Ms. Victoria Bah",
                "custodian_phone": "+237 699 888 999",
            },
            {
                "name": "Autoclave",
                "category": "medical_equipment",
                "brand": "Tuttnauer",
                "model": "A3850",
                "serial_number": "AUTO-STE-001",
                "branch": branches[2],
                "department": "laboratory",
                "purchase_date": base_date + timedelta(days=10),
                "purchase_cost": 8000000,
                "supplier_name": "Laboratory Equipment",
                "status": "in_use",
                "condition": "excellent",
                "custodian_name": "Technician Rose Nyanga",
                "custodian_phone": "+237 699 999 000",
            },
        ]

        admin_user = User.objects.get(username="admin@hospital.cm")

        for data in assets_data:
            branch = data.pop("branch")
            asset, created = Asset.objects.get_or_create(
                serial_number=data["serial_number"],
                defaults={**data, "branch": branch, "created_by": admin_user},
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created asset: {asset.name} ({asset.asset_id})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n✓ Sample data populated successfully!"))
        self.stdout.write("\nDemo Credentials:")
        self.stdout.write("  Super Admin: admin@hospital.cm / Admin123!")
        self.stdout.write("  Branch Manager: manager@hospital.cm / Manager123!")
        self.stdout.write("  Inventory Officer: officer@hospital.cm / Officer123!")
