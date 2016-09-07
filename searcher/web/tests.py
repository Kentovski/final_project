import mock
from django.test import TestCase

# Create your tests here.
from web.views import IndexView, ResultsView, StatisticView, CheckTaskView, SendRequestView


class TestIndexView(TestCase):
    pass


class TestResultsView(TestCase):

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_get(self):
        pass

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_get_object(self):
        pass

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_get_context_data(self):
        pass

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_get_context_data(self):
        pass

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_validate_object(self):
        pass


class TestStatisticView(TestCase):
    pass


class TestCheckTaskView(TestCase):
    pass

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_validate_object(self):
        pass


class TestSendRequestView(TestCase):

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_post_new(self, reverse_mock, redis_mock, task_mock):
        # Set up test data and mock
        task_mock.objects.filter.return_value.order_by.return_value.first.return_value = None
        reverse_mock.return_value = 'test/url'
        task_mock.objects.create.return_value = mock.Mock(id=1)
        request = mock.Mock(POST={'query': 'test'})

        # Run post method
        view_obj = SendRequestView()
        response = view_obj.post(request=request)

        # Verify all the keys has sent to redis
        redis_mock.return_value.lpush.asert_has_calls([
            mock.call('google:search', 'test'),
            mock.call('yandex:search', 'test'),
            mock.call('instagram:search', 'test'),
        ])

        # Verify create is called and only once
        task_mock.objects.create.assert_called_once_with(query='test')

        # Verify the content of response
        self.assertEquals(
            response.content,
            '{"status": "success", "check_url": "test/url", "task_id": 1}'
        )

    @mock.patch('web.views.SpiderTask')
    @mock.patch('web.views.Redis')
    @mock.patch('web.views.reverse')
    def test_post_cached(self, reverse_mock, redis_mock, task_mock):
        # Set up test data and mock
        cached_task = mock.Mock(id='cached_id')
        task_mock.objects.filter.return_value.order_by.return_value.first.return_value = cached_task
        reverse_mock.return_value = 'test/url/cache'
        request = mock.Mock(POST={'query': 'test'})

        # Run post method
        view_obj = SendRequestView()
        response = view_obj.post(request=request)

        # Verify all the keys has sent to redis
        redis_mock.return_value.lpush.asert_has_calls([
            mock.call('google:search', 'test'),
            mock.call('yandex:search', 'test'),
            mock.call('instagram:search', 'test'),
        ])

        # Verify create is not called
        self.assertEquals([], task_mock.objects.create.mock_calls)

        # Verify the content of responses
        self.assertEquals(
            response.content,
            '{"status": "success", "check_url": "test/url/cache", "task_id": "cached_id"}'
        )