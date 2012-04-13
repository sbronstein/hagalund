import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from hagalund import main

        app = main({}, **{"mako.directories":"dragpushpullcom:templates"})
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.settings = app.registry.settings
        self.db = self.settings['mongodb_conn'][self.settings["mongodb.db_name"]]

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from hagalund.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'hagalund')

