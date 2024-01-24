from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from .models import Item, Order, ItemImage, Basket, Category, FeedBack, Tag, Specification, DeliverySettings
from .admin_mixins import ExportAsCSVMixin
from .forms import ItemForm


class ItemImageInLine(admin.TabularInline):
    model = ItemImage
    extra = 3


class FeedbackInline(admin.TabularInline):
    model = FeedBack
    extra = 1


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


class ItemTagsInline(admin.TabularInline):
    model = Item.tags.through
    extra = 1


@admin.action(description='Archived products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Re-archived products')
def remark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.action(description='Set discount 10 percent')
def set_discount_10(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=10)


@admin.action(description='Set discount 5 percent')
def set_discount_5(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(discount=5)


class OrderItemInLine(admin.TabularInline):
    model = Basket
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    def overall_rating(self, obj):
        return obj.calculate_overall_rating()

    list_display = 'name', 'price', 'count', 'description_short', 'archived', 'category', 'available'
    ordering = 'name',
    search_fields = 'name',
    form_class = ItemForm
    inlines = [
        OrderItemInLine,
        FeedbackInline,
        ItemTagsInline,
        ItemImageInLine,
        SpecificationInline,
    ]
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'category', 'available', 'free_delivery'),
        }),
        ('Rating', {
            'fields': ('overall_rating',),
        }),
        ('Price options', {
            'fields': ('price', 'discount', 'count'),
            'description': 'The Price is specified in $',
        }),
    ]
    readonly_fields = ['overall_rating']
    actions = [
        mark_archived,
        remark_archived,
        set_discount_5,
        set_discount_10,
        'export_csv',
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ItemInLine(admin.StackedInline):
    model = Order.items.through
    extra = 1


@admin.action(description='Archived orders')
def mark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='archived')


@admin.action(description='Re-archived orders')
def remark_archived_order(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(status='archived')


@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):
    list_display = 'delivery_type',
    readonly_fields = ('delivery_type',)
    fieldsets = [
        (None, {
            'fields': ('delivery_type',),
        }),
        ('Description', {
            'fields': ('express_delivery_fee', 'free_delivery_threshold', 'standard_delivery_fee'),
        }),
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'customer', 'created_at', 'address', 'status'
    inlines = [
        OrderItemInLine,
    ]
    actions = [
        mark_archived_order,
        remark_archived_order,
        'export_csv',
    ]
    readonly_fields = ('created_at', 'customer', 'address', 'city', 'payment_type', 'total_amount')
    fieldsets = [
        (None, {
            'fields': ('customer', 'created_at', 'total_amount'),
        }),
        ('Description', {
            'fields': ('address', 'city', 'payment_type', 'status'),
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('customer').prefetch_related('items')

    def user_verbose(self, obj: Order) -> str:
        return obj.customer_name.first_name or obj.customer_name.username

    def total_amount_display(self, obj):
        return obj.total_amount

    total_amount_display.short_description = 'Total Amount'
    total_amount_display.admin_order_field = 'total_amount'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_path', 'image')
    list_filter = ('parent_category',)
    search_fields = ('title',)

    def full_path(self, obj):
        path = [obj.title]
        current = obj.parent_category
        while current:
            path.insert(0, current.title)
            current = current.parent_category
        full_path = '/'.join(path)
        last_item = path[-1]
        full_path = full_path.replace(last_item, f'<strong>{last_item}</strong>', 1)

        return format_html(full_path)

    full_path.short_description = 'Full Path'



