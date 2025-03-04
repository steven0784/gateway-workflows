# Copyright 2019 BlueCat Networks (USA) Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

# Various Flask framework items.
import os
import sys
import codecs

from flask import url_for, redirect, render_template, flash, g, jsonify
from wtforms.validators import URL, DataRequired
from wtforms import StringField, PasswordField, SubmitField

from bluecat.wtform_extensions import GatewayForm
from bluecat import route, util
import config.default_config as config
from main_app import app

from .sp_watcher import SPWatcher


def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(__file__))

class GenericFormTemplate(GatewayForm):
    """
    Generic form Template

    Note:
        When updating the form, remember to make the corresponding changes to the workflow pages
    """
    workflow_name = 'service_point_watcher'
    workflow_permission = 'service_point_watcher_page'

    text=util.get_text(module_path(), config.language)
    invalid_url_message=text['invalid_url_message']
    require_message=text['require_message']

    # DNS Edge Pane
    edge_url = StringField(
        label=text['label_config_url'],
        validators=[URL(message=invalid_url_message)],
        render_kw={"placeholder": "https://api-<Edge Instance>.bluec.at"}
    )
    edge_username = StringField(
        label=text['label_config_username'],
        validators=[DataRequired(message=require_message)]
    )
    edge_password = PasswordField(
        label=text['label_config_password']
    )
    execution_interval = StringField(
        label=text['label_config_interval'],
        validators=[DataRequired(message=require_message)]
    )

    submit = SubmitField(label=text['label_submit'])



# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/service_point_watcher/service_point_watcher_endpoint')
@util.workflow_permission_required('service_point_watcher_page')
@util.exception_catcher
def service_point_watcher_service_point_watcher_page():
    form = GenericFormTemplate()
    sp_watcher = SPWatcher.get_instance()

    value = sp_watcher.get_value('edge_url')
    if value is not None:
        form.edge_url.data = value
    value = sp_watcher.get_value('edge_username')
    if value is not None:
        form.edge_username.data = value
    value = sp_watcher.get_value('edge_password')
    if value is not None:
        form.edge_password.data = value
    value = sp_watcher.get_value('execution_interval')
    if value is not None:
        form.execution_interval.data = str(value)

    return render_template(
        'service_point_watcher_page.html',
        form=form,
        text=util.get_text(module_path(), config.language),
        options=g.user.get_options(),
    )


@route(app, '/service_point_watcher/load_col_model')
@util.workflow_permission_required('service_point_watcher_page')
@util.exception_catcher
def load_col_model():
    text=util.get_text(module_path(), config.language)

    nodes = [
        {'index':'id', 'name':'id', 'hidden':True, 'sortable':False},
        {
            'label': text['label_col_name'], 'index':'name', 'name':'name',
            'width':260, 'sortable':False
        },
        {
            'label': text['label_col_ipaddress'], 'index':'ipaddress', 'name':'ipaddress',
            'width':140, 'sortable':False
        },
        {
            'label': text['label_col_site'], 'index':'site', 'name':'site',
            'width':200, 'sortable':False
        },
        {
            'label': text['label_col_connected'], 'index':'connected', 'name':'connected',
            'width':100, 'align':'center', 'sortable':False,
            'formatter': 'select',
            'formatoptions': {
                'value': {'CONNECTED': '✅', 'DISCONNECTED': '❎'}
            }
        },
        {
            'label': text['label_col_status'], 'index':'status', 'name':'status',
            'width':80, 'align':'center', 'sortable':False,
            'formatter': 'select',
            'formatoptions': {
                'value': {'UNKNOWN': '⚪', 'UNREACHED': '🚫', 'GOOD': '🔵', 'BAD': '🔴'}
            }
        }
    ]
    return jsonify(nodes)

@route(app, '/service_point_watcher/load_service_points')
@util.workflow_permission_required('service_point_watcher_page')
@util.exception_catcher
def load_service_points():
    print('Load Service Points is called!!!!')
    sp_watcher = SPWatcher.get_instance()
    service_points = sp_watcher.get_service_points()
    return jsonify(service_points)

@route(app, '/service_point_watcher/form', methods=['POST'])
@util.workflow_permission_required('service_point_watcher_page')
@util.exception_catcher
def service_point_watcher_service_point_watcher_page_form():
    form = GenericFormTemplate()
    sp_watcher = SPWatcher.get_instance()
    text=util.get_text(module_path(), config.language)

    if form.validate_on_submit():
        print(form.submit.data)
        sp_watcher.set_value('edge_url', form.edge_url.data)
        sp_watcher.set_value('edge_username', form.edge_username.data)
        if form.edge_password.data != '':
            sp_watcher.set_value('edge_password', form.edge_password.data)
        sp_watcher.set_value('execution_interval', int(form.execution_interval.data))

        sp_watcher.save()
        g.user.logger.info('SAVED')
        flash(text['saved_message'], 'succeed')
        sp_watcher.register_job()
        return redirect(url_for('service_point_watcherservice_point_watcher_service_point_watcher_page'))
    else:
        g.user.logger.info('Form data was not valid.')
        return render_template(
            'service_point_watcher_page.html',
            form=form,
            text=util.get_text(module_path(), config.language),
            options=g.user.get_options(),
        )
