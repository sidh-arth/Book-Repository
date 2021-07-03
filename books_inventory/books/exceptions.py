from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = {
            'status_code': "400",
            'status': False,
            'message': "Validation error",
            'data': {}
        }

        if(isinstance(response.data,dict)):
            for key, value in response.data.items():#for handling dictionaries
                error = {key: value}
                customized_response['data'].update(error)
        response.data = customized_response
    return response