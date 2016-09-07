# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Item, SpiderTask, Statistic


class ItemAdmin(admin.ModelAdmin):
    list_display = ('url', 'image_source', 'source', 'number', 'task')
    model = Item


class SpiderTaskAdmin(admin.ModelAdmin):
    list_display = ('query', 'is_google_done', 'is_yandex_done', 'is_instagram_done')
    model = SpiderTask


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('query', 'amount')
    model = Statistic

admin.site.register(Item, ItemAdmin)
admin.site.register(SpiderTask, SpiderTaskAdmin)
admin.site.register(Statistic, StatisticAdmin)
