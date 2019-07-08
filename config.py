# Copyright 2019 BlueCat Networks. All rights reserved.

#!/usr/bin/python

import logging


# Name of customer's logo file (can be None) which is stored in static/img.
logo_file = 'resources/images/bluecat-logo.png'

# Run in debug mode, must not do this in a production environment.
debug = False

# List on all interfaces. Only relevant when running standalone rather than under Apache control.
listen_on = '127.0.0.1'

# Where to connect to the API. api_url can be a single address or a list of BAM alias, address tuples.
# Only the name will be shown to the user selecting which BAM to connect to on the login page.
# api_url = [('BAM1 Alias', 'http://172.27.19.203/Services/API?wsdl'),
#            ('BAM2 Alias', 'http://172.27.19.1/Services/API?wsdl')]
api_url = 'http://10.244.140.76/Services/API?wsdl'

# Autologin options
autologin = False
autologin_module_path = None

# Path to directory containing certificates to validate against when connecting to BAM via HTTPS.
# The directory must have been processed with the c_rehash utility supplied with OpenSSL.
# This path is relative to your mounted <bluecat_gateway> folder.
# Only one of certificate_dir_path or certificate_path will be used if both are set, with certificate_dir_path taking
# precedence.
certificate_dir_path = 'customizations/certificates/'

# Path to certificate bundle to validate against when connecting to BAM via HTTPS.
# This path is relative to your mounted <bluecat_gateway> folder.
# Only one of certificate_dir_path or certificate_path will be used if both are set, with certificate_dir_path taking
# precedence.
certificate_path = ''
certificate_upload_time = ''

# Whether to validate the server certificate - this will need to be False for self signed certs
validate_server_cert = False

# Whether to attempt to stop browser autocomplete for passwords. This isn't foolproof, browsers
# try very hard to stop you doing this for good reasons. However, some corporate security
# policies attempt to mandate this so here we are.
block_password_autocomplete = False

# TSIG key file for DDNS updates. Set to '= None' if securing DDNS by source IP rather than by TSIG key.
tsig_key = 'bluecat_portal/tsig-keys/example_key.key'

# Client specific key used to encrypt login cookies
secret_key = 'one fish two fish red fish blue fish'

# Default configuration to pre-select
default_configuration = 'test_config'

# Default view to use
default_view = 'default'

# Logging level
log_level = logging.INFO

# Session logging options
log_session_format = '[%(asctime)s][PID:%(process)d][{username}] %(levelname)s: %(message)s'
log_session_level = logging.DEBUG
log_redirect_to_stdout = False
log_session_path = ''
log_session_timestamp_format = '%Y-%m-%dT%H:%M:%SZ'
log_file_timestamp_format = '%Y-%m-%dT%H%M%S%fZ'

# language setting
language = 'en'

# Auto-reloading changes to workflow modules
module_reload = False

# Shows python deprecation warnings
show_python_deprecation_warnings = True

# Email support
MAIL_SERVER = 'smtp.mail.example.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'example@example.com'
MAIL_DEFAULT_SENDER = 'example@example.com'
MAIL_PASSWORD_PATH = None
ADMINS = ['example_admin@example.com']

# MongoDB support
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'example_DB'
MONGO_USERNAME = None
MONGO_PASSWORD_PATH = None

# Third-party libraries path. Any extra python modules you wish to use in the Gateway must be placed in this directory.
# Those modules will then be available to be imported into workflows. This path is relative to your <bluecat_gateway> folder.
additional_libraries_path = 'customizations/integrations'

# Custom HTML Templates path. Any HTML templates inside this path can be found when importing from a workflow's html.
# This path is relative to your <bluecat_gateway> folder.
custom_html_path = 'customizations/html'

# Color theme of the Gateway website UI. Create your own custom theme and upload it using the Configuration workflow.
ui_theme = 'original_dark_theme'

# The path to the ui_customizations.json file used in the above ui_theme parameter.
ui_customizations_file = 'customizations/ui_customizations.json'

# hash value of ui_customizations_file
ui_customizations_file_hash = ''

# if set, endpoint GET <bluecat_gateway>/serverstatus will return server statistics
enable_serverstatus = True

# Banner message
login_banner = ''
