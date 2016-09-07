# -*- coding: utf-8 -*-

import time
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from django.views.generic import View, TemplateView, DetailView, ListView
from web.models import SpiderTask, Statistic

from django.http.response import JsonResponse, Http404
from redis import Redis
from logger import log


class IndexView(TemplateView):
    """
    Start page view
    """
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        """
        Logging for entering the start page
        """
        log.info('Entered index.html')
        return super(IndexView, self).get(*args, **kwargs)


class ResultsView(DetailView):
    """
    Result page view.
    """
    model = SpiderTask
    template_name = 'results.html'
    slug_field = 'query'
    slug_url_kwarg = 'query'

    def get(self, *args, **kwargs):
        """
        Logging for entering the start page
        :return: result page
        """
        log.info('Entered results.html')
        return super(ResultsView, self).get(*args, **kwargs)

    def get_object(self, queryset=None,):
        """
        Gets last task with the keyword=queryset
        :param queryset: keyword for picture search
        :return: last task with keyword=queryset or raise Http404
        """
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = self.model.objects.filter(query=slug).order_by('-done_time').first()
        self._validate_object(obj)
        return obj

    def get_context_data(self, **kwargs):
        """
        From last task with the keyword gets all images and sorts them by 'number'
        :return: sorted images by 'number'
        """
        ctx = super(ResultsView, self).get_context_data(**kwargs)
        ctx['images'] = self.object.item_set.order_by('number')
        return ctx

    def _validate_object(self, obj):
        """
        Check the task with the keyword.
        :param obj: task with keyword
        :return: Raise Http404 if there is no task with that keyword
        """
        if not obj:
            log.exception('Error HTTP 404. Query=%s', self.kwargs.get(self.slug_url_kwarg))
            raise Http404


class StatisticView(ListView):
    """
    Statistic page view.
    """
    model = Statistic
    context_object_name = 'done_tasks'
    template_name = 'statistic.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Statistic.objects.filter(amount__gte=0).order_by('-amount')


class CheckTaskView(View):
    """
    Check status of task view
    """
    max_loop = 30

    def get(self, request, task_id):
        """
        Get from cache or creates new task and write to cache tasks query
        """
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
    """
    View class of making requests
    """
    redis_keys = ('google:search', 'yandex:search', 'instagram:search')
    key_format = '{query}::{task}'

    def post(self, request):
        """
        Get keyword from request and return json with new or cached task.
        """
        self._query = request.POST.get('query')
        self._update_statistic()
        task = self._get_cached() or self._get_new()
        return JsonResponse(
            {'status': 'success', 'task_id': task.id, 'check_url': reverse('check_task', args=[task.id])}
        )

    def _update_statistic(self):
        """
        Update statistic
        """
        try:
            task = Statistic.objects.get(query=self._query)
            task.amount += 1
            task.save()
        except (KeyError, Statistic.DoesNotExist):
            task = Statistic.objects.create(query=self._query, amount=1)

    def _get_new(self):
        """
        Create a new task with the keyword
        :return: new task with the keyword
        """
        task = SpiderTask.objects.create(query=self._query)
        self._sent_task(task)
        log.info('Created new task. Task.id=%s. Query=%s', task.id, task.query)
        return task

    def _get_cached(self):
        """
        Get last cached result for 1 hour with the keyword
        :return: cached result if it exist
        """
        gte_time = timezone.now() - timedelta(seconds=settings.RESULT_CACHE_TIME)
        cached_query = SpiderTask.objects.filter(query=self._query, done_time__gte=gte_time).order_by('-done_time')
        cached_item = cached_query.first()
        if cached_item:
            log.info('Get cached item. Query=%s', cached_item.query)
        return cached_item

    def _sent_task(self, task):
        """
        Send task to redis
        """
        client = Redis(**settings.REDIS_CONNECTION)
        for key in self.redis_keys:
            client.lpush(key, self.key_format.format(query=str(self._query), task=task.id))
            log.info('Sent task. Task.id=%s. Query=%s', task.id, task.query)
