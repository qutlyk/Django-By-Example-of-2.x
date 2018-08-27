
import sys
import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
# from django.core.urlresolvers import reverse # 2.0以前
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem

# Register your models here.

def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)

	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# write the header row
	writer.writerow([field.verbose_name for field in fields])
	# write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to CSV'

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))
# order_detail.allow_tags = True

class OrderItemInline(admin.TabularInline):
	"""docstring for OrderItemInline"""
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	"""docstring for OrderAdmin"""
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail]
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]
	actions = [export_to_csv]
admin.site.register(Order, OrderAdmin)
