from django.conf import settings

class RenderStrategyUtils(object):

    @classmethod
    def render_input_dict(cls, enqueued_object):
        return {
            'host': settings.RENDER_SERVICE_URL,
            'port': int(settings.RENDER_SERVICE_PORT),
            'owner': settings.RENDER_SERVICE_USER,
            'project': enqueued_object.get_render_project_name(),
            'client_scripts': settings.RENDER_CLIENT_SCRIPTS
        }

    @classmethod
    def collection_dict(cls, enqueued_object):
        return {
            'service_host': "{}:{}".format(
                settings.RENDER_SERVICE_URL,
                settings.RENDER_SERVICE_PORT),
            'baseURL': "http://{}:{}/render-ws/v1".format(
                settings.RENDER_SERVICE_URL,
                settings.RENDER_SERVICE_PORT),
            'owner': settings.RENDER_SERVICE_USER,
            'project': enqueued_object.get_render_project_name(),
            'renderbinPath': settings.RENDER_CLIENT_SCRIPTS
        }
