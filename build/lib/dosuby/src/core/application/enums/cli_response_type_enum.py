class CliResponseTypeEnums:
    SUCCESS = { 'label': 'Success', 'value': True, 'status_code': 'OK'}
    SYSTEM_ERROR = { 'label': 'SystemError', 'value': False, 'status_code': 'FAILED'}
    PARAMETERS_ERROR = { 'label': 'ParametersError', 'value': False, 'status_code': 'FAILED'}
    RESOURCE_ERROR = { 'label': 'ResourceError', 'value': False, 'status_code': 'FAILED'}
    ERROR = { 'label': 'ERROR EXCEPTION', 'value': False, 'status_code': 'FAILED'}