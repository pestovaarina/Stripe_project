from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from .models import Item, Discount, ItemsOrder, Order, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'currency',
        'description'
    )


class ItemsOrderFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_items = any(form.cleaned_data for form in self.forms)
        if not has_items:
            raise ValidationError('Необходим хотя бы один товар.')


class ItemsOrderInline(admin.StackedInline):
    model = ItemsOrder
    formset = ItemsOrderFormSet
    extra = 1
    fields = ('order', 'item', 'amount')


class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    fields = ('name', 'percentage', 'order', 'redeem_by')
    list_display = ('name', 'percentage', 'order', 'redeem_by')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')
    inlines = (ItemsOrderInline,)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'percentage', 'inclusive')


admin.site.register(Item, ItemAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tax, TaxAdmin)
