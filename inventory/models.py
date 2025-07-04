from django.db import models
from django.contrib.auth.models import User

class Entity(models.Model):
    entity_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entity_name

    class Meta:
        verbose_name_plural = "Entities"

class Brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand

class ModelName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Personnel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Position(models.Model):
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position

class FundCluster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Item(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('disposed', 'Disposed'),
    ]

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    fund_cluster = models.ForeignKey(FundCluster, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(ModelName, on_delete=models.SET_NULL, null=True, blank=True)
    serial_no = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    inventory_item_no = models.CharField(max_length=100, unique=True)
    estimated_useful_life = models.PositiveIntegerField(help_text="In years", null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    received_by = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_items')
    received_by_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_positions')
    received_by_date = models.DateField(null=True, blank=True)
    receive_from = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='given_items')
    receive_from_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='given_positions')
    receive_from_date = models.DateField(null=True, blank=True)
    purchase_order_no = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.name} ({self.inventory_item_no})"

class Computer(models.Model):
    entity_name =  models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)
    custody = models.CharField(max_length=100, null=True, blank=True)
    mr = models.CharField(max_length=100, null=True, blank=True)
    room = models.CharField(max_length=50, null=True, blank=True)
    unit_no = models.CharField(max_length=50, null=True, blank=True)
    motherboard = models.CharField(max_length=50, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    processor = models.CharField(max_length=50, null=True, blank=True)
    video_card_0 = models.CharField(max_length=50, null=True, blank=True)
    video_card_1 = models.CharField(max_length=50, null=True, blank=True)
    ram = models.CharField(max_length=50, null=True, blank=True)
    ram_slot = models.CharField(max_length=50, null=True, blank=True)
    mouse = models.CharField(max_length=50, null=True, blank=True)
    keyboard = models.CharField(max_length=50, null=True, blank=True)
    monitor_model = models.CharField(max_length=50, null=True, blank=True)
    monitor_serial_number = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)

    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('offline', 'Offline'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    last_maintenance = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Computer {self.room}-{self.unit_no} ({self.processor})"

class Office(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AccomplishedBy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WorkOrderRequest(models.Model):
    TYPE_CHOICES = [
        ('desktop', 'Desktop'),
        ('laptop', 'Laptop'),
        ('printer', 'Printer'),
        ('scanner', 'Scanner'),
        ('others', 'Others (specify)'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    campus = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    datetime_started = models.DateTimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    action_taken = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    datetime_completed = models.DateTimeField(blank=True, null=True)
    requested_by = models.CharField(max_length=100)
    accomplished_by = models.ForeignKey(AccomplishedBy, on_delete=models.SET_NULL, null=True, blank=True)
    conformed_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Work Order for {self.item} ({self.type})" 