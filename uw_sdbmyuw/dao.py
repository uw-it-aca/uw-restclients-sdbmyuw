# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import ssl
from os.path import abspath, dirname
from restclients_core.dao import DAO


class Sdbmyuw_DAO(DAO):
    def service_name(self):
        return 'sdbmyuw'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def get_service_setting(self, key, default=None):
        # sdb_MYUW uses a DH key which caused
        # SSLError: DH_KEY_TOO_SMALL dh key too small (_ssl.c:1007).
        # Set ssl_context on the connection pool
        if key == "SSL_CONTEXT":
            sdb_ssl_context = ssl.SSLContext()
            sdb_ssl_context.set_ciphers('HIGH:!DH:!aNULL')
            return sdb_ssl_context
        return super().get_service_setting(key, default)
