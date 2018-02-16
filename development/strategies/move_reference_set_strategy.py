# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from django.conf import settings
from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.strategies.chmod_strategy import ChmodStrategy
import logging


class MoveReferenceSetStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.move_reference_set_strategy')

    def get_input(self, ref_set, storage_directory, task):
        extra_flags = ['--remove-source-files']

        if settings.DRY_RUN is True:
            extra_flags.append('--dry-run')
        
        extra_flags_string = ' '.join(extra_flags)

        input_data = {
            'from': ref_set.storage_directory,
            'to': ref_set.get_storage_directory(
                settings.LONG_TERM_BASE_FILE_PATH),
            'extra': extra_flags_string
        }

        return input_data

    def on_finishing(self, ref_set, results, task):
        if settings.DRY_RUN is not True:
            ref_set.storage_directory = \
                ref_set.get_storage_directory(
                    settings.LONG_TERM_BASE_FILE_PATH)
            ChmodStrategy.add_chmod_file(
                ref_set, ref_set.storage_directory)
            ChmodStrategy.add_chmod_dir(
                ref_set, ref_set.storage_directory)
            ChmodStrategy.enqueue_reference(ref_set)
