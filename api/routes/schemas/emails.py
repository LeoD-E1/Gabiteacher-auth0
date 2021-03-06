from constants import EMAIL_REGEX

schema = {
    'send_email': {
        'paths': '/api/email',
        'methods': ['POST'],
        'body': {
            'from_email': {'type': 'string', 'regex': EMAIL_REGEX},
            'from_name': {'type': 'string'},
            'to': {'required': True, 'type': ['string', 'list']},
            'subject': {'required': True, 'type': 'string'},
            'html': {'required': True, 'type': 'string'},
            'text': {'required': True, 'type': 'string'}
        }
    },
    'send_email_template': {
        'paths': '/api/email/<template_name>',
        'methods': ['POST'],
        'body': {
            'from_email': {'type': 'string', 'regex': EMAIL_REGEX},
            'from_name': {'type': 'string'},
            'to': {'required': True, 'type': ['string', 'list'], 'regex': EMAIL_REGEX},
            'subject': {'required': True, 'type': 'string'},
            'data': {'required': True, 'type': 'dict'}
        },
        'params': {
            'template_name': {'required': True, 'type': 'string'}
        }
    },
    'preview_email_template': {
        'paths': '/api/email/<template_name>/preview/<view>',
        'methods': ['GET'],
        'params': {
            'template_name': {'required': True, 'type': 'string'},
            'view': {'required': True, 'allowed': ['html', 'text']}
        }
    }
}
