import os
from unittest.mock import Mock, AsyncMock

from tornado import testing

from waterbutler.server.app import make_app
from waterbutler.server.api.v1.provider import ProviderHandler

from tests.server.api.v1.fixtures import http_request
from tests.utils import MockProvider, MockFileMetadata, MockCoroutine


class ServerTestCase(testing.AsyncHTTPTestCase):

    def get_url(self, path):
        return super().get_url(os.path.join('/v1', path.lstrip('/')))

    def get_app(self):
        return make_app(debug=False)


def mock_handler(http_request):
    """
    Mock WB Provider Handler.

    Since tornado 5.0, handler cannot be shared between tests as fixtures when the testing tornado
    web server is started with ``autoreload=True``, which is enabled automatically if debug mode is
    on. Although setting either ``autoreload==False`` or ``Debug=False`` fixes the issue, it is
    still better to take this mock handler out from fixtures.

    :param http_request: the mocked HTTP request that is required to start the tornado web app
    :return: a mocked handler
    """
    handler = ProviderHandler(make_app(True), http_request)
    handler.path_kwargs = {'provider': 'test', 'path': '/file', 'resource': 'guid1'}
    handler.path = '/test_path'
    handler.provider = MockProvider()
    handler.requested_version = None
    handler.resource = 'test_source_resource'
    handler.metadata = MockFileMetadata()
    handler.dest_path = '/test_dest_path'
    handler.dest_provider = MockProvider()
    handler.dest_resource = 'test_dest_resource'
    handler.dest_meta = MockFileMetadata()
    handler.arguments = {}
    handler.write = Mock()
    handler.write_stream = MockCoroutine()
    handler.redirect = Mock()
    handler.rsock = Mock()
    handler.wsock = Mock()
    handler.rfd = Mock()
    handler.wfd = Mock()
    handler.writer = Mock()
    handler.writer.wait_closed = AsyncMock()
    return handler
