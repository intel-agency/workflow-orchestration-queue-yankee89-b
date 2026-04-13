"""
Tests for OS-APOW Health Check API Router
"""



class TestHealthRouter:
    """Tests for the health check API router."""

    def test_health_router_imports(self):
        """Test that the health router can be imported."""
        from src.os_apow.api.health import router

        assert router is not None

    def test_health_check_endpoint(self):
        """Test the health check endpoint returns expected structure."""
        from src.os_apow.api.health import health_check

        result = health_check()
        assert result["status"] == "online"
        assert result["system"] == "OS-APOW"

    def test_root_endpoint(self):
        """Test the root endpoint returns API info."""
        from src.os_apow.api.health import root

        result = root()
        assert result["name"] == "OS-APOW"
        assert "version" in result
        assert result["docs"] == "/docs"

    def test_health_router_has_routes(self):
        """Test that the health router has the expected routes."""
        from src.os_apow.api.health import router

        route_paths = [route.path for route in router.routes]
        assert "/health" in route_paths
        assert "/" in route_paths
