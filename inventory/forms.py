from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
from cProfile import label
from types import ModuleType
from django import forms
from .models import Item, Computer, WorkOrderRequest, Office, AccomplishedBy, Borrower

class ItemForm(forms.ModelForm):
    UNIT_CHOICES = [
        ("pc/s", "pc/s"),
        ("unit/s", "unit/s"),
        ("ream/s", "ream/s"),
        ("box/es", "box/es"),
        ("set/s", "set/s"),
        ("pack/s", "pack/s"),
        ("meter/s", "meter/s"),
        ("cart/s", "cart/s"),
        ("tube/s", "tube/s"),
        ("bottle/s", "bottle/s"),
        ("other", "Other")
    ]
    unit = forms.ChoiceField(choices=UNIT_CHOICES, required=True)
    class Meta:
        model = Item
        fields = [
            'entity', 'fund_cluster', 'name', 'category', 'quantity', 'unit', 'unit_cost', 'description',
            'brand', 'model', 'serial_no', 'expiry_date', 'inventory_item_no', 'estimated_useful_life',
            'supplier', 'received_by', 'received_by_position', 'received_by_date',
            'receive_from', 'receive_from_position', 'receive_from_date',
            'purchase_order_no', 'status', 'custody'
        ]
        widgets = {
            'received_by_date': forms.DateInput(attrs={'type': 'date'}),
            'receive_from_date': forms.DateInput(attrs={'type': 'date'}),
        } 

class ComputerForm(forms.ModelForm):
    CUSTODY_CHOICES = [
        ("TSG", "TSG")
    ]
    custody = forms.ChoiceField(choices=CUSTODY_CHOICES, required=False)
    
    mr = forms.CharField(max_length=100, required=False, label="Memorandum Receipt")
    
    ROOM_CHOICES = [
        ("EB204", "EB204"),
        ("EB205", "EB205"), 
        ("EB206", "EB206"),
        ("EB207", "EB207"), 
        ("EB208", "EB208"), 
        ("EB209", "EB209"),
        ("EB210", "EB210")
    ]
    room = forms.ChoiceField(choices=ROOM_CHOICES, required=True)

    PC_UNIT_CHOICES = [(str(i), str(i)) for i in range(0, 21)]
    unit_no = forms.ChoiceField(choices=PC_UNIT_CHOICES, required=True)

    LAB_EQUIP_CHOICES = [
        ("Desktop Computer (Teacher's Table)", "Desktop Computer (Teacher's Table)"),
        ("Desktop Computer", "Desktop Computer")
    ]
    lab_equipment = forms.ChoiceField(choices=LAB_EQUIP_CHOICES, required=True)
    
    OPERATING_SYSTEM_CHOICES = [
        ("Windows 11", "Windows 11"),
        ("Windows 10", "Windows 10")
    ]
    operating_system = forms.ChoiceField(choices=OPERATING_SYSTEM_CHOICES, required=True)
    
    SOURCE_CHOICES = [
        ("License", "License")
    ]
    source = forms.ChoiceField(choices=SOURCE_CHOICES, required=True)
    
    MOTHERBOARD_CHOICES = [
        ("B660M DS3H DDR4", "B660M DS3H DDR4"),
        ("HP 280 G3 MT", "HP 280 G3 MT")
    ]
    motherboard = forms.ChoiceField(choices=MOTHERBOARD_CHOICES, required=True)
    
    PROCESSOR_CHOICES = [
        ("Intel Core i5 12th Gen", "Intel Core i5 12th Gen"),
        ("Intel Core i5-7500", "Intel Core i5-7500")
    ]
    processor = forms.ChoiceField(choices=PROCESSOR_CHOICES, required=True)

    STORAGE_CHOICES = [
        ("128GB SSD", "128GB SSD"),
        ("256GB SSD", "256GB SSD"),
        ("500GB SSD", "500GB SSD"),
        ("None", "None")
    ]
    storage = forms.ChoiceField(choices=STORAGE_CHOICES, required=True)

    VIDEO_CARD_0_CHOICES = [
        ("RTX 2060 - 20GB", "RTX 2060 - 20GB"),
        ("RTX 2060 - 16GB", "RTX 2060 - 16GB"),
        ("Intel UHD Graphics 770 - 4GB", "Intel UHD Graphics 770 - 4GB"),
        ("Intel UHD Graphics 770 - 8GB", "Intel UHD Graphics 770 - 8GB"),
        ("Intel HD Graphics 630 - 4GB", "Intel HD Graphics 630 - 4GB"),
        ("GeForce GT 730 - 10GB", "GeForce GT 730 - 10GB"),
        ("GeForce GT 730 - 6GB", "GeForce GT 730 - 6GB"),
        ("No Video Card", "No Video Card")
    ]
    video_card_0 = forms.ChoiceField(choices=VIDEO_CARD_0_CHOICES, required=True)

    VIDEO_CARD_1_CHOICES = [
        ("GeForce RTX 2060 - 16GB", "GeForce RTX 2060 - 16GB"),
        ("Intel UHD Graphics 770 - 4GB", "Intel UHD Graphics 770 - 4GB"),
        ("Intel UHD Graphics 770 - 8GB", "Intel UHD Graphics 770 - 8GB"),
        ("Intel HD Graphics 630 - 8GB", "Intel HD Graphics 630 - 8GB"),
        ("No Video Card", "No Video Card")
    ]
    video_card_1 = forms.ChoiceField(choices=VIDEO_CARD_1_CHOICES, required=True)

    RAM_CHOICES = [
        ("16GB", "16GB"),
        ("8GB", "8GB")
    ]
    ram = forms.ChoiceField(choices=RAM_CHOICES, required=True)

    RAM_SLOT_CHOICES = [
        ("1 of 2 slots used", "1 of 2 slots used"),
        ("2 of 2 slots used", "2 of 2 slots used"),
        ("1 of 4 slots used", "1 of 4 slots used"),
        ("2 of 4 slots used", "2 of 4 slots used")
    ]
    ram_slot = forms.ChoiceField(choices=RAM_SLOT_CHOICES, required=True)

    YES_NO_CHOICES = [("yes", "Yes"), ("no", "No")]
    mouse = forms.ChoiceField(choices=YES_NO_CHOICES, required=True)
    keyboard = forms.ChoiceField(choices=YES_NO_CHOICES, required=True)

    MONITOR_MODEL_CHOICES = [
        ("EG24S1", "EG24S1"),
        ("V226HQL", "V226HQL"),
        ("EG24S1 Pro", "EG24S1 Pro"),
        ("HP P223", "HP P223"),
        ("None", "None")
    ]
    monitor_model = forms.ChoiceField(choices=MONITOR_MODEL_CHOICES, required=True)
    monitor_serial_number = forms.CharField(max_length=100, required=True)

    remarks = forms.CharField(max_length=200, required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Computer
        fields = [
            'entity_name', 'custody', 'mr', 'room', 'unit_no', 'lab_equipment', 'operating_system', 'source', 'motherboard', 'storage', 'processor', 'video_card_0', 'video_card_1', 'ram', 'ram_slot',
            'mouse', 'keyboard', 'monitor_model', 'monitor_serial_number', 'remarks', 'status', 'last_maintenance'
        ]
        widgets = {
            'last_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkOrderRequestForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRequest
        fields = [
            'item', 'campus', 'office', 'datetime_started', 'type', 'description',
            'requested_by', 'accomplished_by', 'conformed_by', 'action_taken', 'remarks', 'datetime_completed'
        ]
        widgets = {
            'datetime_started': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_completed': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'action_taken': forms.Textarea(attrs={'rows': 2}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = [
            'item', 'borrower_lname', 'borrower_fname', 'borrower_mi', 'campus', 'office', 'datetime_borrowed', 
            'purpose', 'action_taken', 'remarks', 'datetime_returned', 'approved_by'
        ]
        widgets = {
            'datetime_borrowed': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'datetime_returned': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 