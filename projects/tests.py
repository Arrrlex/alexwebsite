from django.test import TestCase
from projects.logic.pi import calculate_pi
from projects.logic.e import calculate_e
from projects.logic.fibonacci import fib_str
from projects.logic.prime_factors import write_prime_factors
from django.core.urlresolvers import reverse

class PiViewTests(TestCase):

	def test_pi_50(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'50', 'fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "3.1415926535897932384626433832795028841971693993751")

	def test_pi_nothing(self):
		response = self.client.get(reverse('projects:karan'), {'fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number")

	def test_pi_empty_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'', 'fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_pi_invalid_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'I am not a number','fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_pi_too_big(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")

	def test_pi_too_small(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'calculate_pi'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")

class KaranScriptsTests(TestCase):

	def test_pi_50(self):
		self.assertEqual(calculate_pi(50), "3.1415926535897932384626433832795028841971693993751")

	def test_e_50(self):
		self.assertEqual(calculate_e(50), "2.7182818284590452353602874713526624977572470936999")

	def test_fib_50(self):
		self.assertEqual(fib_str(50), "12586269025")

	def test_prime_factors_50(self):
		self.assertEqual(write_prime_factors(50), "2 &times; 5<sup>2</sup>")

class EViewTests(TestCase):

	def test_e_50(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'50', 'fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "2.7182818284590452353602874713526624977572470936999")

	def test_e_nothing(self):
		response = self.client.get(reverse('projects:karan'), {'fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number")

	def test_e_empty_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'', 'fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_e_invalid_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'I am not a number','fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_e_too_big(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")

	def test_e_too_small(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'calculate_e'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")

class FibViewTests(TestCase):

	def test_fib_50(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'50', 'fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "12586269025")

	def test_fib_nothing(self):
		response = self.client.get(reverse('projects:karan'), {'fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number")

	def test_fib_empty_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'', 'fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_fib_invalid_string(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'I am not a number','fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a valid number")

	def test_fib_too_big(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")

	def test_fib_too_small(self):
		response = self.client.get(reverse('projects:karan'), {'arg':'4000', 'fun':'fib_str'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Please enter a number between 1 and 1000")