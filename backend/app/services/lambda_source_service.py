class LambdaSourceService:
    """Placeholder interface for future lambda value sourcing integrations."""

    def search_lambda(self, component_name: str, context: str | None = None) -> dict:
        return {
            "component_name": component_name,
            "status": "not_implemented",
            "message": "Lambda lookup service is a placeholder in MVP.",
            "context": context or "",
        }
