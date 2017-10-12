import argschema
#import renderapi

class RenderModuleException(Exception):
    """Base Exception class for render module"""
    pass


class RenderClientParameters(argschema.schemas.DefaultSchema):
    host = argschema.fields.Str(
        required=True, description='render host')
    port = argschema.fields.Int(
        required=True, description='render post integer')
    owner = argschema.fields.Str(
        required=True, description='render default owner')
    project = argschema.fields.Str(
        required=True, description='render default project')
    client_scripts = argschema.fields.Str(
        required=True, description='path to render client scripts')
    memGB = argschema.fields.Str(
        required=False, default='5G',
        description='string describing java heap memory (default 5G)')


class RenderParameters(argschema.ArgSchema):
    render = argschema.fields.Nested(
        RenderClientParameters,
        required=True,
        description="parameters to connect to render server")


# this is deprecated and unnecessary now, leaving it in to minimize rewrite
class ArgSchemaModule(argschema.ArgSchemaParser):
    def __init__(self, *args, **kwargs):
        super(ArgSchemaModule, self).__init__(
            *args, **kwargs)
        self.logger.warning("DEPRECATED: please just use \
            argschema.ArgSchemaParser which has this functionality")



class RenderModule(argschema.ArgSchemaParser):
    default_schema = RenderParameters

    def __init__(self, schema_type=None, *args, **kwargs):
        if (schema_type is not None and not issubclass(
                schema_type, RenderParameters)):
            raise RenderModuleException(
                'schema {} is not of type RenderParameters')

        # TODO do we want output schema passed?
        super(RenderModule, self).__init__(
            schema_type=schema_type, *args, **kwargs)
        #self.render = renderapi.render.connect(**self.args['render'])