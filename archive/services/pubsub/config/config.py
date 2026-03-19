import os


class Settings:
    """
    Settings for the pub/sub application.
    """
    project_id = os.getenv("PROJECTID", "default-project-id")
    server_port = os.getenv("PORT", "8080")
    subscriptions = ["injective-sub"]  # Placeholders for actual subscription info


settings = Settings()
