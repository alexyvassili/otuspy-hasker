from rest_framework import renderers
from openapi_codec import OpenAPICodec
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import CoreJSONRenderer


class SwaggerRenderer(renderers.BaseRenderer):
    media_type = 'application/openapi+json'
    format = 'swagger'

    def render(self, data, media_type=None, renderer_context=None):
        codec = OpenAPICodec()
        return codec.dump(data)




schema_view = get_schema_view(title="Hasker API",
                              # renderer_classes=[CoreJSONRenderer, SwaggerRenderer]
                              )

