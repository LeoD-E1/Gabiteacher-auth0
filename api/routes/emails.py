from cerberus import Validator as get_check
from os.path import isdir, basename
from flask import render_template
from glob import glob
from importlib import import_module

from api.commons.emails import send
from api.commons.root_dir import root_dir

_templates_namespace = 'templates.emails'
_templates_path = root_dir + '/' + '/'.join(_templates_namespace.split('.'))
_template_dirs = glob(f'{_templates_path}/*')
templates = {}
for tdir in _template_dirs:
    if (not isdir(tdir)):
        continue
    name = basename(tdir)
    template = {}
    spec = import_module(f'{_templates_namespace}.{name}.spec').spec
    preview_data = import_module(
        f'{_templates_namespace}.{name}.preview_data').preview_data
    template['html_path'] = f'emails/{name}/html.html'
    template['text_path'] = f'emails/{name}/text.txt'
    template['preview_data'] = preview_data
    template['check'] = get_check(spec)
    templates[name] = template


def send_email(req):
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    text = req['body']['text']
    html = req['body']['html']
    result = send(to, subject, text, html)
    return {'status': 200, 'body': result}


def send_email_template(req):
    name = req['params']['template_name']
    if (name not in templates):
        return {'status': 404, 'body': {'message': f"Template '{name}' not found"}}
    template = templates[name]
    to = req['body']['to']
    to = [to] if type(to) == str else to
    subject = req['body']['subject']
    data = req['body']['data']
    check = template['check']
    if (not check(data)):
        return {'status': 400, 'body': {'message': f"Invalid Data for template '{name}'", 'errors': check.errors}}
    html = render_template(template['html_path'], data=data)
    text = render_template(template['text_path'], data=data)
    result = send(to, subject, text, html)
    return {'status': 200, 'body': result}


def preview_email_template(req):
    name = req['params']['template_name']
    view = req['params']['view']
    if name not in templates:
        return {'status': 404, 'body': {'message': f"Template '{name}' not found"}}
    template = templates[name]
    data = template['preview_data']
    if view == 'html':
        return render_template(template['html_path'], data=data)
    elif view == 'text':
        return render_template(template['text_path'], data=data)