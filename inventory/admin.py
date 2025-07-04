from django.contrib import admin
from .models import Category, Item, Computer, Entity, Brand, ModelName, Supplier, Personnel, Position, FundCluster, Office, AccomplishedBy, WorkOrderRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'inventory_item_no', 'supplier', 'received_by', 'status',
        'entity', 'fund_cluster', 'quantity', 'unit', 'unit_cost', 'cost', 'brand', 'model', 'serial_no',
        'expiry_date', 'estimated_useful_life', 'received_by_position', 'received_by_date',
        'receive_from', 'receive_from_position', 'receive_from_date', 'purchase_order_no'
    )
    list_filter = ('status', 'category', 'supplier', 'brand', 'entity', 'fund_cluster', 'unit')
    search_fields = ('name', 'inventory_item_no', 'description', 'serial_no')

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('room', 'unit_no', 'motherboard', 'storage', 'processor', 'status', 'last_maintenance')
    list_filter = ('status', 'room')
    search_fields = ('room', 'unit_no', 'motherboard', 'processor', 'remarks')

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_name', 'created_at', 'updated_at')
    search_fields = ('entity_name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand',)
    search_fields = ('brand',)

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position',)
    search_fields = ('position',)

@admin.register(FundCluster)
class FundClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AccomplishedBy)
class AccomplishedByAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WorkOrderRequest)
class WorkOrderRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'campus', 'office', 'datetime_started', 'type', 'requested_by', 'accomplished_by', 'datetime_completed')
    list_filter = ('type', 'campus', 'office', 'accomplished_by')
    search_fields = ('item__name', 'description', 'requested_by', 'accomplished_by__name', 'conformed_by')

