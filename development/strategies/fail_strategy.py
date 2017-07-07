from workflow_engine.strategies import execution_strategy
from development.models import Numberr

class FailStrategy(execution_strategy.ExecutionStrategy):

	#override if needed
	#get the data for the input file
	def get_input(self, enqueued_object):
		raise Exception('This should fail - Workfow test case')

		return input_data