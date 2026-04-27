"""
Tests for OS-APOW Webhook API Router
"""


class TestWebhookRouter:
    """Tests for the webhook API router."""

    def test_webhook_router_imports(self):
        """Test that the webhook router can be imported."""
        from src.os_apow.api.webhook import router

        assert router is not None
        assert router.prefix == "/webhook"

    def test_webhook_router_has_routes(self):
        """Test that the webhook router has the expected routes."""
        from src.os_apow.api.webhook import router

        route_paths = [route.path for route in router.routes]
        assert "/webhook/github" in route_paths
