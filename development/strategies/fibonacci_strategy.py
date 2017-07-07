from workflow_engine.strategies import execution_strategy
from development.models import Numberr

class FibonacciStrategy(execution_strategy.ExecutionStrategy):

	#override if needed
	#called after the execution finishes
	#process and save results to the database
	def on_finishing(self, enqueued_object, results):
		enqueued_object.fibonacci = results['fibonacci']
		enqueued_object.save()

	#override if needed
	#get the data for the input file
	def get_input(self, enqueued_object):
		input_data = {}
		input_data['number'] = enqueued_object.value

		return input_data

	#override if needed
	def get_objects_for_queue(self, job):
		objects = []
		enqueued_object = job.get_enqueued_object()
		objects.append(enqueued_object)

		for prime in enqueued_object.primes.all():
			objects.append(prime)

		return objects