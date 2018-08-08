from django.apps import AppConfig


class JobsAppConfig(AppConfig):

    name = "chemflow.jobs"
    verbose_name = "Jobs"

    def ready(self):
        try:
            import jobs.signals  # noqa F401
        except ImportError:
            pass
