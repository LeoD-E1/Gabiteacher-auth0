schema = {
    'send_email': {
        'paths': '/api/mail',
        'methods': ['POST'],
        'body': {
            'to': {'required': True},
            'subject': {'required': True},
            'html': {'required': True},
            'text': {'required': True}
        }
    }
}
