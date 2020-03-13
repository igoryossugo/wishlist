from unittest import mock

from genie.factory import build_app


def test_build_app_should_pre_startup():
    with mock.patch('genie.factory.pre_startup') as pre_startup:
        build_app()

    assert pre_startup.called


def test_build_app_should_setup_routes():
    with mock.patch('genie.factory.setup_routes') as setup_routes:
        build_app()

    assert setup_routes.called
