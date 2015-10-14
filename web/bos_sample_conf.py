# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Configuration for bos samples.
"""

#!/usr/bin/env python
#coding=utf-8

#import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

#PROXY_HOST = 'localhost:8080'

HOST = 'agostop.sinaapp.com'
AK = 'f4f896541b9e4083b69392c0e0d4e645'
SK = 'b11293dfa76b43d3b73d3f324cbc5bd2'

#logger = logging.getLogger('baidubce.services.bos.bosclient')
#fh = logging.FileHandler('sample.log')
#fh.setLevel(logging.INFO)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
#logger.setLevel(logging.DEBUG)
#logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)