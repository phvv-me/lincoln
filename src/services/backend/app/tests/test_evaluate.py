from ..handlers.evaluate import evaluation_handler


def test_evaluate():
    assert evaluation_handler(None, None) is not None
