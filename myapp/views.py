from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import Http404
from .models import Branch, Asset, UserRole
from .forms import BranchForm, AssetForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def get_user_role(user):
    if user.is_superuser:
        return "super_admin"
    try:
        return user.role.role
    except UserRole.DoesNotExist:
        return None


def user_has_permission(user, asset_or_branch):
    role = get_user_role(user)

    if role == "super_admin":
        return True

    if isinstance(asset_or_branch, Asset):
        branch = asset_or_branch.branch
    else:
        branch = asset_or_branch

    if hasattr(user, "role") and user.role.branch:
        return user.role.branch == branch

    return False


@login_required
def dashboard(request):
    role = get_user_role(request.user)

    if role == "super_admin":
        total_branches = Branch.objects.count()
        total_assets = Asset.objects.count()
        recent_assets = Asset.objects.all()[:5]
        assets_by_status = Asset.objects.values("status").annotate(count=Count("id"))
    else:
        if not hasattr(request.user, "role") or not request.user.role.branch:
            branch = None
        else:
            branch = request.user.role.branch

        total_branches = 1 if branch else 0
        total_assets = Asset.objects.filter(branch=branch).count() if branch else 0
        recent_assets = Asset.objects.filter(branch=branch)[:5] if branch else []
        assets_by_status = (
            Asset.objects.filter(branch=branch)
            .values("status")
            .annotate(count=Count("id"))
            if branch
            else []
        )

    context = {
        "total_branches": total_branches,
        "total_assets": total_assets,
        "recent_assets": recent_assets,
        "assets_by_status": assets_by_status,
        "role": role,
    }

    return render(request, "dashboard.html", context)


@login_required
def branch_list(request):
    role = get_user_role(request.user)

    if role not in ["super_admin", "branch_manager"]:
        messages.error(request, "You do not have permission to view branches.")
        return redirect("dashboard")

    branches = Branch.objects.all()
    return render(request, "branches/list.html", {"branches": branches})


@login_required
def branch_add(request):
    role = get_user_role(request.user)

    if role != "super_admin":
        messages.error(request, "Only Super Admins can add branches.")
        return redirect("branch_list")

    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch added successfully.")
            return redirect("branch_list")
    else:
        form = BranchForm()

    return render(request, "branches/form.html", {"form": form, "title": "Add Branch"})


@login_required
def branch_edit(request, branch_id):
    role = get_user_role(request.user)

    if role != "super_admin":
        messages.error(request, "Only Super Admins can edit branches.")
        return redirect("branch_list")

    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Branch updated successfully.")
            return redirect("branch_list")
    else:
        form = BranchForm(instance=branch)

    return render(
        request,
        "branches/form.html",
        {"form": form, "branch": branch, "title": "Edit Branch"},
    )


@login_required
def asset_list(request):
    role = get_user_role(request.user)
    search_query = request.GET.get("search", "")
    filter_branch = request.GET.get("branch", "")
    filter_status = request.GET.get("status", "")

    if role == "super_admin":
        assets = Asset.objects.all()
        branches = Branch.objects.all()
    else:
        if not hasattr(request.user, "role") or not request.user.role.branch:
            assets = Asset.objects.none()
            branches = Branch.objects.none()
        else:
            assets = Asset.objects.filter(branch=request.user.role.branch)
            branches = Branch.objects.filter(id=request.user.role.branch.id)

    if search_query:
        assets = assets.filter(
            Q(name__icontains=search_query) | Q(asset_id__icontains=search_query)
        )

    if filter_branch:
        if role == "super_admin":
            assets = assets.filter(branch_id=filter_branch)

    if filter_status:
        assets = assets.filter(status=filter_status)

    context = {
        "assets": assets,
        "branches": branches,
        "search_query": search_query,
        "filter_branch": filter_branch,
        "filter_status": filter_status,
        "status_choices": Asset._meta.get_field("status").choices,
        "role": role,
    }

    return render(request, "assets/list.html", context)


@login_required
def asset_add(request):
    role = get_user_role(request.user)

    if role not in ["branch_manager", "inventory_officer", "super_admin"]:
        messages.error(request, "You do not have permission to add assets.")
        return redirect("asset_list")

    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user

            if role in ["branch_manager", "inventory_officer"]:
                if not hasattr(request.user, "role") or not request.user.role.branch:
                    messages.error(request, "You must be assigned to a branch.")
                    return redirect("asset_list")
                asset.branch = request.user.role.branch

            asset.save()
            messages.success(request, "Asset added successfully.")
            return redirect("asset_list")
    else:
        form = AssetForm()
        if role in ["branch_manager", "inventory_officer"]:
            if hasattr(request.user, "role") and request.user.role.branch:
                form.fields["branch"].initial = request.user.role.branch
                form.fields["branch"].queryset = Branch.objects.filter(
                    id=request.user.role.branch.id
                )

    return render(request, "assets/form.html", {"form": form, "title": "Add Asset"})


@login_required
def asset_edit(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    role = get_user_role(request.user)

    if not user_has_permission(request.user, asset):
        messages.error(request, "You do not have permission to edit this asset.")
        raise Http404

    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset updated successfully.")
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)
        if role in ["branch_manager", "inventory_officer"]:
            form.fields["branch"].queryset = Branch.objects.filter(id=asset.branch.id)

    return render(
        request,
        "assets/form.html",
        {"form": form, "asset": asset, "title": "Edit Asset"},
    )


@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    if not user_has_permission(request.user, asset):
        messages.error(request, "You do not have permission to view this asset.")
        raise Http404

    return render(request, "assets/detail.html", {"asset": asset})


@login_required
def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    role = get_user_role(request.user)

    if role != "super_admin":
        messages.error(request, "Only Super Admins can delete assets.")
        raise Http404

    if request.method == "POST":
        asset.delete()
        messages.success(request, "Asset deleted successfully.")
        return redirect("asset_list")

    return render(request, "assets/confirm_delete.html", {"asset": asset})
