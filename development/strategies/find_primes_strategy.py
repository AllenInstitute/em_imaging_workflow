from workflow_engine.strategies import execution_strategy
from development.models import Numberr

class FindPrimesStrategy(execution_strategy.ExecutionStrategy):

	#override if needed
	#called after the execution finishes
	#process and save results to the database
	def on_finishing(self, enqueued_object, results):
		primes = results['primes']
		for prime in primes:
			try:
				prime_number = Numberr.object.get(value=int(prime))
			except Exception:
				prime_number = Numberr(value=prime)

			prime_number.is_prime = True
			prime_number.save()

			if not self.has_prime(prime_number, enqueued_object):
				enqueued_object.primes.add(prime_number)

	#override if needed
	#get the data for the input file
	def get_input(self, enqueued_object):
		input_data = {}
		input_data['number'] = enqueued_object.value

		return input_data

	def has_prime(self, prime_number, enqueued_object):
		result = False

		for prime in enqueued_object.primes.all():
			if prime.value == prime_number.value:
				result = True

		return result
