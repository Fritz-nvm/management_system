from django import forms
from django.contrib.auth.models import User
from .models import Branch, Asset, UserRole


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [
            "name",
            "code",
            "city",
            "region",
            "manager_name",
            "manager_phone",
            "status",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Branch Name"}
            ),
            "code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Branch Code"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "region": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Region"}
            ),
            "manager_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Manager Name"}
            ),
            "manager_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Manager Phone"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            "name",
            "category",
            "brand",
            "model",
            "serial_number",
            "branch",
            "department",
            "purchase_date",
            "purchase_cost",
            "supplier_name",
            "status",
            "condition",
            "custodian_name",
            "custodian_phone",
            "user_manual",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Asset Name"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Brand"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Model"}
            ),
            "serial_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Serial Number"}
            ),
            "branch": forms.Select(attrs={"class": "form-select"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "purchase_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "purchase_cost": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Purchase Cost"}
            ),
            "supplier_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Supplier Name"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "custodian_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Custodian Name"}
            ),
            "custodian_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Custodian Phone"}
            ),
            "user_manual": forms.FileInput(attrs={"class": "form-control"}),
        }
