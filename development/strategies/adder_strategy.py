from workflow_engine.strategies import execution_strategy
from development.models import Numberr

class AdderStrategy(execution_strategy.ExecutionStrategy):

	#override if needed
	#called after the execution finishes
	#process and save results to the database
	def on_finishing(self, enqueued_object, results):
		enqueued_object.sum_of_primes = results['sum']
		enqueued_object.save()

	#override if needed
	#get the data for the input file
	def get_input(self, enqueued_object):
		input_data = {}

		numbers = []
		for prime in enqueued_object.primes.all():
			numbers.append(prime.value)

		input_data['numbers'] = numbers

		return input_data