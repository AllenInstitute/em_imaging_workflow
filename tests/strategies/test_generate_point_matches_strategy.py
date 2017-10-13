import django
django.setup()
import pprint
import simplejson as json
from django.test import TestCase
from development.strategies.generate_point_matches_strategy import \
    GeneratePointMatchesStrategy
from render_parameters import *

class TestGeneratePointMatchesStrategy(TestCase):
    def test_schema(self):
        params_dict = dict(
            sparkhome='{{SPARK_HOME}}',
            logdir='{{LOG_DIR}}',
            jarfile='{{JAR_FILE}}'
        )

        schema = PointMatchClientParameters()
        params_file = schema.dump(params_dict)

        params_string = json.dumps(params_file.data, indent=2)

        with open('txt.json', 'w') as f:
            f.write(params_string)

        assert len(params_string) > 0

        params_json = json.loads(params_string)


    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = GeneratePointMatchesStrategy()
        input_json = strategy.get_input(enqueued_object,
                                        storage_directory,
                                        task)

        assert input_json['render']['port'] == 8998

