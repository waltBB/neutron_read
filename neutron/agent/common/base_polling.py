# Copyright 2015 Cloudbase Solutions.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

class BasePollingManager(object):

    # 初始化强制轮询和轮询完成
    def __init__(self): 
        self._force_polling = False
        self._polling_completed = True
    
    # 强制轮询，初始为true
    def force_polling(self):
        self._force_polling = True
    
    # 轮询完成，初始为true
    def polling_completed(self):
        self._polling_completed = True
    
    # 轮询是必须的，抛出不能实现错误
    def _is_polling_required(self):
        raise NotImplementedError()

    @property
    def is_polling_required(self): 
        # Always consume the updates to minimize polling.
        # 总消费的更新来减少轮询
        polling_required = self._is_polling_required()

        # Polling is required regardless of whether updates have been detected.
        # 无论是否发现更新，轮询都是必须的
        if self._force_polling:
            self._force_polling = False
            polling_required = True

        # Polling is required if not yet done for previously detected updates.
        # 如果尚未为先前检测到更新，轮询是必须的
        if not self._polling_completed:
            polling_required = True

        if polling_required:
            # Track whether polling has been completed to ensure that
            # polling can be required until the caller indicates via a
            # call to polling_completed() that polling has been successfully performed.
            # 跟踪轮询是否已经完成，直到调用者可以要求确保投票表明通过调用polling_completed()轮询已成功执行
            self._polling_completed = False

        return polling_required


class AlwaysPoll(BasePollingManager):

    @property
    def is_polling_required(self):
        return True
