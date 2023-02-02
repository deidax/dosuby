class CliResponseTypeEnums:
    SUCCESS = { 'label': 'Success', 'value': True, 'status_code': 'OK'}
    SYSTEM_ERROR = { 'label': 'SystemError', 'value': False, 'status_code': 'ERROR'}
    PARAMETERS_ERROR = { 'label': 'ParametersError', 'value': False, 'status_code': 'ERROR'}
    RESOURCE_ERROR = { 'label': 'ResourceError', 'value': False, 'status_code': 'ERROR'}