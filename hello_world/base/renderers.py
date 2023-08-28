# Third Party Stuff
from rest_framework.renderers import JSONRenderer


class HelloWorldApiRenderer(JSONRenderer):
    media_type = "application/vnd.helloworld+json"
