from django.db import models
from django.contrib.auth.models import User


class UserRole(models.Model):
    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("branch_manager", "Branch Manager"),
        ("inventory_officer", "Inventory Officer"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="inventory_officer"
    )
    branch = models.ForeignKey(
        "Branch", on_delete=models.SET_NULL, null=True, blank=True, related_name="staff"
    )

    class Meta:
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Branch(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=150)
    manager_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Asset(models.Model):
    CATEGORY_CHOICES = [
        ("medical_equipment", "Medical Equipment"),
        ("vehicle", "Vehicle"),
        ("generator", "Generator"),
        ("furniture", "Furniture"),
        ("computer", "Computer"),
        ("other", "Other"),
    ]

    DEPARTMENT_CHOICES = [
        ("emergency", "Emergency"),
        ("surgery", "Surgery"),
        ("maternity", "Maternity"),
        ("pediatrics", "Pediatrics"),
        ("radiology", "Radiology"),
        ("laboratory", "Laboratory"),
        ("administration", "Administration"),
        ("maintenance", "Maintenance"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("in_use", "In Use"),
        ("available", "Available"),
        ("maintenance", "Under Maintenance"),
        ("retired", "Retired"),
    ]

    CONDITION_CHOICES = [
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    asset_id = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=150, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="assets")
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
    supplier_name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="good"
    )
    custodian_name = models.CharField(max_length=150)
    custodian_phone = models.CharField(max_length=20)
    user_manual = models.FileField(upload_to="manuals/", blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assets_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.asset_id})"

    def save(self, *args, **kwargs):
        if not self.asset_id:
            self.asset_id = self.generate_asset_id()
        super().save(*args, **kwargs)

    def generate_asset_id(self):
        import datetime

        count = Asset.objects.count() + 1
        return f"AST-{datetime.datetime.now().year}-{count:05d}"
