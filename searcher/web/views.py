# -*- coding: utf-8 -*-

import time
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from django.views.generic import View, TemplateView, DetailView
from web.models import SpiderTask

from django.http.response import JsonResponse, Http404
from redis import Redis
from logger import log


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        log.info('Entered index.html')
        return super(IndexView, self).get(*args, **kwargs)


class ResultsView(DetailView):
    model = SpiderTask
    template_name = 'results.html'
    slug_field = 'query'
    slug_url_kwarg = 'query'

    def get(self, *args, **kwargs):
        log.info('Entered results.html')
        return super(ResultsView, self).get(*args, **kwargs)

    # достаёт все таски с данным квери
    def get_object(self, queryset=None,):
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = self.model.objects.filter(query=slug).order_by('-done_time').first()
        self._validate_object(obj)
        return obj

    # из данного последнего таска с квери достаёт и сортирует все картинки
    def get_context_data(self, **kwargs):
        ctx = super(ResultsView, self).get_context_data(**kwargs)
        ctx['images'] = self.object.item_set.order_by('number')
        return ctx

    #если нет такого таска - 404
    def _validate_object(self, obj):
        if not obj:
            log.exception('Error HTTP 404. Query=%s', self.kwargs.get(self.slug_url_kwarg))
            raise Http404


class StatisticView(TemplateView):
    template_name = 'statistic.html'


class CheckTaskView(View):
    max_loop = 30

    def get(self, request, task_id):
        task = SpiderTask.objects.get(id=task_id)
        loop_index = 0
        while not task.done_time:
            time.sleep(1)
            task = SpiderTask.objects.get(id=task_id)
            loop_index += 1
            if loop_index >= self.max_loop:
                break
        return JsonResponse({'is_done': bool(task.done_time), 'results_url': reverse('results', args=[task.query])})


class SendRequestView(View):
    redis_keys = ('google:search', 'yandex:search', 'instagram:search')
    key_format = '{query}::{task}'

    def post(self, request):
        self._query = request.POST.get('query')
        # сделать запись в статистик
        task = self._get_cached() or self._get_new()
        return JsonResponse(
            {'status': 'success', 'task_id': task.id, 'check_url': reverse('check_task', args=[task.id])}
        )

    def _get_new(self):
        task = SpiderTask.objects.create(query=self._query)
        self._sent_task(task)
        log.info('Created new task. Task.id=%s. Query=%s', task.id, task.query)
        return task

    def _get_cached(self):
        gte_time = timezone.now() - timedelta(seconds=settings.RESULT_CACHE_TIME)
        cached_query = SpiderTask.objects.filter(query=self._query, done_time__gte=gte_time).order_by('-done_time')
        cached_item = cached_query.first()
        if cached_item:
            log.info('Get cached item. Query=%s', cached_item.query)
        return cached_item

    def _sent_task(self, task):
        client = Redis(**settings.REDIS_CONNECTION)
        for key in self.redis_keys:
            client.lpush(key, self.key_format.format(query=str(self._query), task=task.id))
            log.info('Sent task. Task.id=%s. Query=%s', task.id, task.query)
