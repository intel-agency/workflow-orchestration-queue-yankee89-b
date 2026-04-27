"""
Tests for OS-APOW Worker Service
"""


from src.os_apow.services.worker import WorkerService


class TestWorkerService:
    """Tests for the Worker service facade."""

    def test_worker_service_imports(self):
        """Test that the WorkerService can be imported."""
        assert WorkerService is not None

    def test_worker_service_creation(self):
        """Test creating a WorkerService instance."""
        service = WorkerService()
        assert service.shell_bridge_path == "./scripts/devcontainer-opencode.sh"

    def test_worker_service_custom_bridge_path(self):
        """Test creating a WorkerService with custom bridge path."""
        service = WorkerService(shell_bridge_path="/custom/path.sh")
        assert service.shell_bridge_path == "/custom/path.sh"

    def test_worker_service_import_from_services(self):
        """Test that WorkerService can be imported from services package."""
        from src.os_apow.services import WorkerService as WS

        assert WS is WorkerService
