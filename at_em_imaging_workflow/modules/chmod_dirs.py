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
import simplejson as json
import argparse
import sys
import os


if __name__ == "__main__" and __package__ is None:
    __package__ = "at_em_image_processing.modules.chmod_dirs"

example = {
    'dirs': [ '/path/to/dir1', '/path/to/dir2' ],
    'files': [ '/destination/path' ]
}

class ChmodDirs(object):
    def __init__(self):
        pass

    def chmod_dirs(self, spec):
        for d in spec['dirs']:
            os.system(
                'find %s -type d -print0 | xargs -0 -n1 -P2 chmod go+rx' % (
                    d))
        for d in spec['files']:
            os.system(
                'find %s -type f -print0 | xargs -0 -n1 -P2 chmod go+r' % (
                    d))

    def chmod_dirs2(self, spec):
        for d in spec['dirs']:
            os.system(
                'find %s -type d -print -exec chmod go+rx {} \;' % (
                    d))
        for d in spec['files']:
            os.system(
                'find %s -type f -print -exec chmod go+r {} \;' % (
                    d))

    def parse_json(self, json_string):
        return json.loads(json_string)

    def parse_json_file(self, json_file):
        with open(json_file, 'r') as f:
            return self.parse_json(f.read())

    @classmethod
    def parse_args(cls, args):
        parser = argparse.ArgumentParser(
            description='bulk change directory mode')
        parser.add_argument('--input_json', help='input arguments')
        parser.add_argument('--output_json', help='output results')

        return vars(parser.parse_args(args))
    
    @classmethod
    def main(cls, args):
        parsed_args = ChmodDirs.parse_args(args[1:])

        chmd = ChmodDirs()

        inp = chmd.parse_json_file(parsed_args['input_json'])

        chmd.chmod_dirs(inp)

        with open(parsed_args['output_json'], 'w') as f:
            f.write(json.dumps(inp))


if '__main__' == __name__:
    sys.exit(ChmodDirs.main(sys.argv))