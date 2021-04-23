
import json
import traceback
from functools import wraps
import tornado 
from tornado import web
from tornado_swagger.model import register_swagger_model


def expect_json_data(route_method):
    @wraps(route_method)
    def decorated(self, *args, **kwargs):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception:
            data = None
        if data is None:
            raise RequestInvalid(log_message="Payload is expected to be json!")
        return route_method(self, *args, **kwargs, data=data)
    return decorated


class CoolException(web.HTTPError):
    def __init__(self, *args, status_code=500, log_message=None, **kwargs):
        super().__init__(status_code=status_code, log_message=log_message, *args, **kwargs)
        print(log_message)


class RequestInvalid(web.HTTPError):
    def __init__(self, *args, status_code: int = 400, log_message: str = "Invalid Request", **kwargs):
        super().__init__(status_code=status_code, log_message=log_message, *args, **kwargs)
        print(log_message)


class BaseHandler(web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self._reason = None
        self._status_code = 200

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type,x-requested-with") 
        origin = self.request.headers.get("Origin", None)

        if origin:
            self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header('Access-Control-Allow-Credentials', "true")
        self.set_header('Access-Control-Expose-Headers', "Content-Type")
        self.set_header('Access-Control-Allow-Headers', "access-control-allow-origin,authorization,Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")

   
    def write_ok(self, msg):
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps({'status': {'code': 200, 'message': msg}}))
    def handle_response_error(self, status_code: int, msg):
        self._reason = msg
        return self.write_error(status_code)

    def write_error(self, status_code: int, **kwargs):
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self._status_code = status_code
            self.finish(json.dumps({
                'status': {
                    'code': status_code,
                    'message': self._reason,
                    'traceback': lines,
                }
            }))
        else:
            self._status_code = status_code
            self.finish(json.dumps({
                'status': {
                    'code': status_code,
                    'message': self._reason,
                }
            }))

    def data_received(self, chunk: bytes):
        pass

    def options(self, *args, **kwargs):
        # no body
        self.set_status(204)
        self.finish()

    def export_body_to_dictionary(self, data, required_keys: list):
        missings = []
        return_dict = dict()
        for item in required_keys:
            if item not in data:
                missings.append(item)
            else:
                return_dict[item] = data[item]
        
        return missings, return_dict



@register_swagger_model
class UserLogin:
    """
    ---
    type: object
    description: Cluster operation
    properties:
        user:
            type: string
        password:
            type: string
    """

@register_swagger_model
class ClusterDeletion:
    """
    ---
    type: object
    description: Cluster operation
    properties:
        arn:
            type: string
    """

@register_swagger_model
class WinOperation:
    """
    ---
    type: object
    description: Environment operation
    properties:
        action:
            type: string
            description: the action to do
            enum: [start, stop]

        
    """

@register_swagger_model
class EnvOperation:
    """
    ---
    type: object
    description: Environment operation
    properties:
        action:
            type: string
            description: the action to do
            enum: [start, stop, restore]

        
    """

@register_swagger_model
class ClusterOperation:
    """
    ---
    type: object
    description: Cluster operation
    properties:
        name:
            type: string
        action:
            type: string
            description: the action to do
            enum: [start, stop, describe]
        environment:
            type: string
            description: nvironemt name
            enum: [test, stage, prod]

        
    """


@register_swagger_model
class WinServer:
    """
    ---
    type: object
    description: Windows Server
    properties:
        name:
            type: string
        instance_id:
            type: string
        instance_type:
            type: string
        public_ip_address:
            type: string
        environment:
            type: string
            description: nvironemt name
            enum: [test, stage, prod]
        status:
            type: boolean
        status_name:
            type: string
    """

@register_swagger_model
class NewCluster:
    """
    ---
    type: object
    description: New Cluster
    properties:
        name:
            type: string
        
    """
@register_swagger_model
class ClusterModel:
    """
    ---
    type: object
    description: Cluster model representation
    properties:
        name:
            type: string
        environment:
            type: string
            description: nvironemt name
            enum: [test, stage, prod]
        arn:
            type: string
        state:
            type: string
            description: Cluster ECS state
        status:
            type: boolean
            description: Clinic status
        url:
            type: string

    """
