from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Category, Item, Computer, Entity, Brand, ModelName, Supplier, Personnel, Position, WorkOrderRequest, Borrower, Office, AccomplishedBy
from django.db.models import Count, Sum, IntegerField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import Cast
import json
from .forms import ItemForm, ComputerForm, WorkOrderRequestForm, BorrowerForm
import csv
from django.http import HttpResponse
from typing import TYPE_CHECKING
from docx import Document
import tempfile
from docxtpl import DocxTemplate
from django.utils import timezone
import tempfile
from docxcompose.composer import Composer
if TYPE_CHECKING:
    from .models import Computer

def home(request):
    return render(request, 'home.html', {'show_navbar': False})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get total counts
    total_items = Item.objects.count()  # type: ignore
    total_computers = Computer.objects.count()  # type: ignore[attr-defined]
    
    # Get items by category
    items_by_category = list(Item.objects.values('category__name').annotate(count=Count('id')))  # type: ignore
    
    # Get computer status distribution
    computer_status = list(Computer.objects.values('status').annotate(count=Count('id')))  # type: ignore[attr-defined]
    
    # Get items needing attention (under maintenance or disposed)
    items_needing_attention = Item.objects.filter(  # type: ignore
        status__in=['maintenance', 'disposed']
    ).select_related('category').order_by('status')[:5]
    
    # Get computers needing maintenance
    computers_needing_maintenance = Computer.objects.filter(status='maintenance')[:5]  # type: ignore[attr-defined]
    
    # Prepare data for charts
    chart_data = {
        'items_by_category': json.dumps(items_by_category, cls=DjangoJSONEncoder),
        'computer_status': json.dumps(computer_status, cls=DjangoJSONEncoder),
    }
    
    context = {
        'total_items': total_items,
        'total_computers': total_computers,
        'chart_data': chart_data,
        'items_needing_attention': items_needing_attention,
        'computers_needing_maintenance': computers_needing_maintenance,
    }
    
    return render(request, 'inventory/dashboard.html', context)

@login_required
def item_list(request):
    # Only show items with status available, in_use, or maintenance
    items = Item.objects.filter(status__in=['available', 'in_use', 'maintenance']).select_related('entity', 'category', 'brand', 'model', 'supplier', 'received_by', 'received_by_position', 'receive_from', 'receive_from_position', 'fund_cluster')
    edit_id = request.GET.get('edit')
    form = None
    if request.method == 'POST':
        if edit_id:
            item = get_object_or_404(Item, pk=edit_id)
            form = ItemForm(request.POST, instance=item)
        else:
            form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item saved successfully!')
            return redirect('item_list')
    else:
        if edit_id:
            item = get_object_or_404(Item, pk=edit_id)
            form = ItemForm(instance=item)
        else:
            form = ItemForm()
    return render(request, 'inventory/item_list.html', {'items': items, 'form': form, 'action': 'Edit' if edit_id else 'Add', 'edit_id': edit_id, 'archive': False})

@login_required
def item_archive(request):
    # Only show items with status disposed
    items = Item.objects.filter(status='disposed').select_related('entity', 'category', 'brand', 'model', 'supplier', 'received_by', 'received_by_position', 'receive_from', 'receive_from_position', 'fund_cluster')
    return render(request, 'inventory/item_list.html', {'items': items, 'archive': True})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_detail.html', {
        'item': item
    })

@login_required
def computer_list(request):
    # Get computers grouped by room
    rooms = ['EB204', 'EB205', 'EB206', 'EB207', 'EB208', 'EB209', 'EB210']
    computers_by_room = {}
    
    for room in rooms:
        computers_by_room[room] = Computer.objects.filter(room=room).annotate(
            unit_no_int=Cast('unit_no', IntegerField())
        ).order_by('unit_no_int')  # type: ignore[attr-defined]
    
    return render(request, 'inventory/computer_list.html', {
        'computers_by_room': computers_by_room,
        'rooms': rooms
    })

@login_required
def computer_detail(request, pk):
    computer = get_object_or_404(Computer, pk=pk)  # type: ignore[attr-defined]
    return render(request, 'inventory/computer_detail.html', {
        'computer': computer
    })

def is_superuser(user):
    return user.is_superuser

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully!')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form, 'action': 'Edit', 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@login_required
def add_computer(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Computer added successfully!')
            return redirect('computer_list')
    else:
        form = ComputerForm()
    
    return render(request, 'inventory/computer_form.html', {
        'form': form
    })

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@login_required
def edit_computer(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Computer updated successfully!')
            return redirect('computer_list')
    else:
        form = ComputerForm(instance=computer)
    return render(request, 'inventory/computer_form.html', {'form': form, 'edit': True, 'computer': computer})

def export_computers_csv(request, room=None):  # type: ignore
    if room:
        computers = Computer.objects.filter(room=room)  # type: ignore[attr-defined]
        filename = f"computers_{room}.csv"
    else:
        computers = Computer.objects.all()  # type: ignore[attr-defined]
        filename = "computers_all.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow([
        'Entity Name', 'Custody', 'Memorandum Receipt', 'Room', 'Unit No', 'Motherboard', 'Storage', 'Processor',
        'Video Card 0', 'Video Card 1', 'RAM', 'RAM Slot', 'Mouse', 'Keyboard',
        'Monitor Model', 'Monitor Serial Number', 'Remarks', 'Status', 'Last Maintenance'
    ])
    for c in computers:
        writer.writerow([
            c.entity_name, c.custody, c.mr, c.room, c.unit_no, c.motherboard, c.storage, c.processor,
            c.video_card_0, c.video_card_1, c.ram, c.ram_slot, c.mouse, c.keyboard,
            c.monitor_model, c.monitor_serial_number, c.remarks, c.get_status_display(),
            c.last_maintenance.strftime('%Y-%m-%d') if c.last_maintenance else ''
        ])
    return response 

@login_required
def work_order_request_list(request):
    work_orders = WorkOrderRequest.objects.select_related('item', 'campus', 'office', 'accomplished_by').all().order_by('-datetime_started')  # type: ignore[attr-defined]
    return render(request, 'inventory/work_order_request_list.html', {'work_orders': work_orders})

@login_required
def work_order_request_create(request, item_id=None):
    initial = {}
    if item_id:
        initial['item'] = item_id
    if request.method == 'POST':
        form = WorkOrderRequestForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order Request submitted successfully!')
            return redirect('work_order_request_list')
    else:
        form = WorkOrderRequestForm(initial=initial)
    return render(request, 'inventory/work_order_request_form.html', {'form': form, 'action': 'Add'})

def work_order_request_list_and_add(request):
    item_id = request.GET.get('item_id')
    initial = {}
    if item_id:
        initial['item'] = item_id
    if request.method == 'POST':
        form = WorkOrderRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_order_request_list_and_add')
    else:
        form = WorkOrderRequestForm(initial=initial)
    work_orders = WorkOrderRequest.objects.all().order_by('-datetime_started')
    return render(request, 'inventory/work_order_request_list_and_add.html', {
        'form': form,
        'work_orders': work_orders,
    })

def delete_work_order_request(request, pk):
    work_order = get_object_or_404(WorkOrderRequest, pk=pk)
    if request.method == 'POST':
        work_order.delete()
        return redirect('work_order_request_list_and_add')
    return redirect('work_order_request_list_and_add')

def update_work_order_request(request, pk):
    work_order = get_object_or_404(WorkOrderRequest, pk=pk)
    if request.method == 'POST':
        form = WorkOrderRequestForm(request.POST, instance=work_order)
        if form.is_valid():
            form.save()
            return redirect('work_order_request_list_and_add')
    else:
        form = WorkOrderRequestForm(instance=work_order)
    work_orders = WorkOrderRequest.objects.all().order_by('-datetime_started')
    return render(request, 'inventory/work_order_request_list_and_add.html', {
        'form': form,
        'work_orders': work_orders,
        'edit_id': pk,
    })

def export_work_order_docx(request, pk):
    work_order = get_object_or_404(WorkOrderRequest, pk=pk)
    template_path = 'static/WORK ORDER REQUEST.docx'
    doc = DocxTemplate(template_path)

    context = {
        'wo': {
            'campus': work_order.campus or '',
            'office': work_order.office or '',
            'datetime_started': work_order.datetime_started.strftime('%Y-%m-%d %H:%M'),
            'get_type_display': work_order.get_type_display(),
            'description': work_order.description or '',
            'requested_by': work_order.requested_by or '',
            'actions_taken': work_order.action_taken or '',
            'remarks': work_order.remarks or '',
            'datetime_completed': work_order.datetime_completed.strftime('%Y-%m-%d %H:%M') if work_order.datetime_completed else '',
            'accomplished_by': work_order.accomplished_by.name if work_order.accomplished_by else '',
            'conformed': work_order.conformed_by or '',
        }
    }
  
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=work_order_{work_order.pk}.docx'
        return response 

@login_required
def borrower_list(request):
    borrowers = Borrower.objects.select_related('item').all()
    return render(request, 'inventory/borrower_list.html', {'borrowers': borrowers})

@login_required
def borrower_form(request):
    edit_id = request.GET.get('edit_id')
    item_id = request.GET.get('item_id')
    borrower_instance = None
    initial = {}
    if item_id:
        initial['item'] = item_id
    if edit_id:
        borrower_instance = get_object_or_404(Borrower, pk=edit_id)
    if request.method == 'POST':
        if edit_id and borrower_instance:
            form = BorrowerForm(request.POST, instance=borrower_instance)
        else:
            form = BorrowerForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Borrower record saved successfully!')
            form = BorrowerForm()  # Reset form after save
            edit_id = None
            borrower_instance = None
    else:
        if borrower_instance:
            form = BorrowerForm(instance=borrower_instance)
        else:
            form = BorrowerForm(initial=initial)
    borrowers = Borrower.objects.select_related('item', 'campus', 'office', 'approved_by').all()
    return render(request, 'inventory/borrower_list_form.html', {
        'form': form,
        'items': Item.objects.all(),
        'entities': Entity.objects.all(),
        'offices': Office.objects.all(),
        'accomplished_by_list': AccomplishedBy.objects.all(),
        'borrowers': borrowers,
        'edit_id': edit_id,
        'selected_item_id': item_id,
    })

@login_required
def item_transaction_select(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_transaction_select.html', {'item': item})

ROOMS = ['204', '205', '206', '207', '208', '209', '210']

def reports_view(request):
    computers = list(Computer.objects.values(
        'unit_no', 'lab_equipment', 'operating_system', 'source', 'status', 'room',
        'motherboard', 'storage', 'processor', 'video_card_0', 'video_card_1', 'ram', 'ram_slot',
        'mouse', 'keyboard', 'monitor_model', 'monitor_serial_number', 'remarks'
    ))
    # Prepare inventory items for reporting
    items = Item.objects.select_related('entity', 'fund_cluster', 'category', 'supplier').all()
    inventory_items = [
        {
            'no': item.id,
            'entity': item.entity.entity_name if item.entity else '-',
            'fund_cluster': item.fund_cluster.name if item.fund_cluster else '-',
            'name': item.name,
            'category': item.category.name if item.category else '-',
            'quantity': item.quantity,
            'unit': item.unit,
            'unit_cost': str(item.unit_cost) if item.unit_cost is not None else '-',
            'description': item.description or '-',
            'expiry_date': item.expiry_date.strftime('%Y-%m-%d') if item.expiry_date else '-',
            'inventory_item_no': item.inventory_item_no,
            'estimated_useful_life': item.estimated_useful_life if item.estimated_useful_life is not None else '-',
            'supplier': item.supplier.name if item.supplier else '-',
            'custody': item.custody if item.custody else '-',
            'status': item.status,
            'status_display': item.get_status_display(),
        }
        for item in items
    ]
    return render(request, 'reports.html', {
        'rooms': ROOMS,
        'computers': json.dumps(computers),
        'inventory_items': json.dumps(inventory_items),
    })

# Helper function for functionality report context
def get_functionality_report_context(room):
    return {
        'room': room,
        'today': timezone.now().strftime('%B %d, %Y'),
        'computers': [
            {
                'unit_no': c.unit_no,
                'lab_equipment': c.lab_equipment,
                'operating_system': c.operating_system,
                'source': c.source,
                'status': c.status,
            }
            for c in Computer.objects.filter(room=f'EB{room}')
        ]
    }

def export_functionality_report_docx(request, room):
    template_path = 'static/Functionality Report.docx'  # Updated to match user path
    doc = DocxTemplate(template_path)
    context = get_functionality_report_context(room)
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=functionality_report_EB{room}.docx'
        return response

def get_components_inventory_report_context(room):
    return {
        'room': room,
        'today': timezone.now().strftime('%B %d, %Y'),
        'computers': [
            {
                'unit_no': c.unit_no,
                'motherboard': c.motherboard,
                'storage': c.storage,
                'processor': c.processor,
                'video_card_0': c.video_card_0,
                'video_card_1': c.video_card_1,
                'ram': c.ram,
                'ram_slot': c.ram_slot,
                'mouse': c.mouse,
                'keyboard': c.keyboard,
                'monitor_model': c.monitor_model,
                'monitor_serial_number': c.monitor_serial_number,
                'status': c.status,
                'remarks': c.remarks
            }
            for c in Computer.objects.filter(room=f'EB{room}')
        ]
    }

def export_components_inventory_docx(request, room):
    template_path = 'static/Components Inventory Report.docx'
    doc = DocxTemplate(template_path)
    context = get_components_inventory_report_context(room)
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=components_report_EB{room}.docx'
        return response

def get_functionality_report_context_all():
    rooms = ROOMS
    all_computers = []
    for room in rooms:
        computers = [
            {
                'unit_no': c.unit_no,
                'lab_equipment': c.lab_equipment,
                'operating_system': c.operating_system,
                'source': c.source,
                'status': c.status,
            }
            for c in Computer.objects.filter(room=f'EB{room}')
        ]
        all_computers.append({'room': room, 'computers': computers})
    return {
        'rooms': all_computers,
        'today': timezone.now().strftime('%B %d, %Y'),
    }

def export_functionality_report_docx_all(request):
    template_path = 'static/Functionality Report.docx'
    doc = DocxTemplate(template_path)
    context = get_functionality_report_context_all()
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=functionality_report_all_rooms.docx'
        return response

def export_inventory_item_docx(request):
    status = request.GET.get('status', 'all')
    if status == 'all':
        items = Item.objects.select_related('category').all()
    else:
        items = Item.objects.select_related('category').filter(status=status)
    context = {
        'status': status,
        'today': timezone.now().strftime('%B %d, %Y'),
        'items': [
            {
                'id': item.id,
                'name': item.name,
                'category': item.category.name if item.category else '',
                'quantity': item.quantity,
                'unit': item.unit,
                'unit_cost': str(item.unit_cost) if item.unit_cost is not None else '',
                'status': item.status,
                'status_display': item.get_status_display(),
            }
            for item in items
        ]
    }
    template_path = 'static/Inventory Item Report.docx'  # Use your inventory item report template
    doc = DocxTemplate(template_path)
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=inventory_item_report_{status}.docx'
        return response

def export_borrowers_docx(request):
    borrowers = Borrower.objects.select_related('item', 'campus', 'office', 'approved_by').all()
    context = {
        'today': timezone.now().strftime('%B %d, %Y'),
        'borrowers': [
            {
                'id': b.pk,
                'item_name': b.item.name if b.item else '',
                'borrower_name': b.borrower_lname + ',' + b.borrower_fname + b.borrower_mi,
                'campus': b.campus.entity_name if b.campus else '-',
                'office': b.office.name if b.office else '-',
                'datetime_borrowed': b.datetime_borrowed.strftime('%Y-%m-%d %H:%M'),
                'purpose': b.purpose,
                'action_taken': b.get_action_taken_display(),
                'remarks': b.remarks,
                'datetime_returned': b.datetime_returned.strftime('%Y-%m-%d %H:%M') if b.datetime_returned else '-',
                'approved_by': b.approved_by.name if b.approved_by else '-',
            }
            for b in borrowers
        ]
    }
    template_path = 'static/BORROWER REQUEST.docx'  # Use your borrower report template
    doc = DocxTemplate(template_path)
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=borrowers_report.docx'
        return response

def export_borrower_docx(request, pk):
    borrower = get_object_or_404(Borrower.objects.select_related('item', 'campus', 'office', 'approved_by'), pk=pk)
    borrower_name = f"{borrower.borrower_lname}, {borrower.borrower_fname} {borrower.borrower_mi}".strip()
    context = {
        'today': timezone.now().strftime('%B %d, %Y'),
        'borrower': {
            'id': borrower.pk,
            'item_name': borrower.item.name if borrower.item else '',
            'borrower_name': borrower_name,
            'campus': borrower.campus.entity_name if borrower.campus else '-',
            'office': borrower.office.name if borrower.office else '-',
            'datetime_borrowed': borrower.datetime_borrowed.strftime('%Y-%m-%d %H:%M'),
            'purpose': borrower.purpose,
            'action_taken': borrower.get_action_taken_display(),
            'remarks': borrower.remarks,
            'datetime_returned': borrower.datetime_returned.strftime('%Y-%m-%d %H:%M') if borrower.datetime_returned else '-',
            'approved_by': borrower.approved_by.name if borrower.approved_by else '-',
        }
    }
    template_path = 'static/BORROWER REQUEST.docx'  # Use your borrower request template
    doc = DocxTemplate(template_path)
    doc.render(context)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
        doc.save(tmp.name)
        tmp.seek(0)
        response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=borrower_request_{pk}.docx'
        return response