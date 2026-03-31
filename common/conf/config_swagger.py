from common.conf.settings import settings
from common.core.enums import ServiceEnum

CONFIG_SWAGGER = {
    "title": "Oak",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "swagger_ui_parameters": {"operationsSorter": "method"},
    "version": '1.0.0',
    "description": """
        Description.
    """,
}

SVC_DOCS_SETTINGS = {
    ServiceEnum.OAK: settings.oak_app,
}


def get_swagger_config(service_name: ServiceEnum) -> dict:
    # Avoid mutating the module-level default config dict.
    config = dict(CONFIG_SWAGGER)
    app_settings = SVC_DOCS_SETTINGS.get(service_name)
    config['docs_url'] = f'{app_settings.docs_prefix}/docs'
    config['redoc_url'] = f'{app_settings.docs_prefix}/redoc'
    config['description'] = app_settings.description
    config['version'] = app_settings.version
    config['title'] = app_settings.name
    config['openapi_url'] = f'{app_settings.docs_prefix}/openapi.json'
    return config
