# Copyright (C) 2013 Aniket Panse <contact@aniketpanse.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Aniket Panse <contact@aniketpanse.in> grants Johnny Vestergaard <jkv@unixcluster.dk>
# a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable
# copyright license to reproduce, prepare derivative works of, publicly
# display, publicly perform, sublicense, relicense, and distribute [the] Contributions
# and such derivative works.


import gevent.monkey

gevent.monkey.patch_all()
from gevent.server import StreamServer

import unittest
import os
import shutil
import tempfile

from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.client.models.session import BaitSession
from beeswarm.drones.client.baits.http import Http
from beeswarm.drones.honeypot.capabilities import http as honeypot_http


class HttpTest(unittest.TestCase):
    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_login(self):
        """ Tests if HTTP bait can login to the http capability.
        """

        options = {'enabled': 'True', 'port': 0, 'users': {'test': 'test'}}
        cap = honeypot_http.Http(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1',
            'honeypot_id': '1234'
        }

        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'

        current_bait = Http(bait_info)
        current_bait.start()
        srv.stop()


if __name__ == '__main__':
    unittest.main()
