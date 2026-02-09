import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from openpyxl.styles import Font
import openpyxl
from .models import Asset
from datetime import datetime


def link_callback(uri, rel):
    """Convert HTML temporary urls to absolute system paths for xhtml2pdf"""
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    else:
        return uri
    return path


def export_assets_pdf(request):
    assets = Asset.objects.all()

    now = datetime.now()
    current_inventory_period = now.strftime("%B %Y").upper()
    template_path = "assets_pdf_template.html"
    context = {
        "assets": assets,
        "report_period": current_inventory_period,
        "generated_at": now,
    }

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="inventory_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response


def export_assets_excel(request):
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="assets_inventory.xlsx"'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Assets"

    # 1. Define Headers (Exactly matching your <thead>)
    columns = [
        "Asset ID",
        "Name",
        "Branch",
        "Department",
        "Manufacturer",
        "Serial Number",
        "Purchase Date",
        "Custodian Name",
        "Custodian Phone",
        "Status",
        "Condition",
        "Cost",
    ]
    ws.append(columns)

    # 2. Make Headers Bold
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # 3. Pull Data and Map to Columns
    # Using select_related('branch') to avoid N+1 database queries
    assets = Asset.objects.all().select_related("branch")

    for asset in assets:
        ws.append(
            [
                asset.asset_id,
                asset.name,
                str(asset.branch),
                asset.get_department_display(),  # Assuming choices
                asset.brand,  # Maps to "Manufacturer"
                asset.serial_number,
                asset.purchase_date.strftime("%Y-%m-%d") if asset.purchase_date else "",
                asset.custodian_name,
                asset.custodian_phone,
                asset.get_status_display(),
                asset.get_condition_display(),
                asset.purchase_cost,
            ]
        )

    # 4. Optional: Auto-adjust column widths for readability
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column].width = adjusted_width

    wb.save(response)
    return response
