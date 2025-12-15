import subprocess
import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')
FOOOCUS_URL = os.getenv('FOOOCUS_URL', 'http://127.0.0.1:8888/docs')

class ServerRunner:
	def __init__(self):
		raw_fooocus_path: str = os.getenv('FOOOCUS_API_PATH', '')
		if not raw_fooocus_path:
			raise ValueError(
				'Configuration Error: `FOOOCUS_API_PATH` is missing.\n' +
				'Create a .env file based on .env.example and set the path.'
			)
		self.fooocus_dir: Path = Path(raw_fooocus_path).resolve()

		# Detect OS for correct Python path inside venv
		if os.name == 'nt':
			self.venv_python = self.fooocus_dir / 'venv' / 'Scripts' / 'python.exe'
		else:
			self.venv_python = self.fooocus_dir / 'venv' / 'bin' / 'python'

		# Process handles
		self.proc_ollama: subprocess.Popen | None = None
		self.proc_fooocus: subprocess.Popen | None = None

		# OWNERSHIP FLAGS (Default to False)
		# If True, we started it, so we must kill it.
		# If False, it was already there, so we leave it alone.
		self.owns_ollama: bool = False
		self.owns_fooocus: bool = False

	def _is_service_running(self, name: str, url: str) -> bool:
		'''Checks if a service is already online.'''
		try:
			requests.get(url, timeout=1)
			print(f'{name} is already online. Attaching...')
			return True
		except requests.ConnectionError:
			return False

	def _wait_for_service(self, name: str, url: str, retries: int = 30) -> bool:
		'''Waits for a newly started service to come online.'''
		print(f'Waiting for {name} to warm up...', end='\r')
		for _ in range(retries):
			try:
				requests.get(url, timeout=1)
				print(f'✅ {name} is Ready!')
				return True

			except requests.ConnectionError:
				time.sleep(2)

		print(f'\n❌ Timeout waiting for {name}.')

		return False

	def __enter__(self) -> None:
		print('🚀 Checking AI Infrastructure...')

		# --- 1. OLLAMA LOGIC ---
		if self._is_service_running('Ollama', OLLAMA_URL):
			self.owns_ollama = False
		else:
			print('Starting Ollama (CPU Mode)...')
			# Apply the CPU-Only fix
			ollama_env = os.environ.copy()
			ollama_env['CUDA_VISIBLE_DEVICES'] = ''

			try:
				self.proc_ollama = subprocess.Popen(
					['ollama', 'serve'],
					env=ollama_env,
					stdout=subprocess.DEVNULL,
					stderr=subprocess.PIPE
				)

				self.owns_ollama = True

				# Wait for it to actually start
				if not self._wait_for_service('Ollama', OLLAMA_URL):
					sys.exit(1)
			except FileNotFoundError:
				print('❌ Error: Ollama not installed.')
				sys.exit(1)


		# --- 2. FOOOCUS LOGIC ---
		if self._is_service_running('Fooocus-API', FOOOCUS_URL):
			self.owns_fooocus = False
		else:
			print('Starting Fooocus-API...')
			if not os.path.exists(self.venv_python):
				print(f'❌ Error: Python not found at {self.venv_python}')
				# If we started Ollama, kill it before exiting
				if self.proc_ollama and self.owns_ollama:
					self.proc_ollama.terminate()
				sys.exit(1)

			self.proc_fooocus = subprocess.Popen(
				[self.venv_python, 'main.py'],
				cwd=self.fooocus_dir,
				stdout=subprocess.DEVNULL,
				stderr=subprocess.PIPE,
				shell=False
			)
			self.owns_fooocus = True

			if not self._wait_for_service('Fooocus', FOOOCUS_URL):
				# Cleanup if Fooocus fails
				if self.proc_ollama and self.owns_ollama:
					self.proc_ollama.terminate()
				sys.exit(1)

	def __exit__(self, exc_type, exc_val, exc_tb):
		print('\n🧹 Finalizing...')

		# Only kill Fooocus if we started it
		if self.owns_fooocus and self.proc_fooocus:
			print('   🔻 Stopping Fooocus...', end=' ')
			self.proc_fooocus.terminate()
			try:
				self.proc_fooocus.wait(timeout=5)
			except subprocess.TimeoutExpired:
				self.proc_fooocus.kill()
			print('Done.')
		else:
			print('Fooocus left running (External process).')

		# Only kill Ollama if we started it
		if self.owns_ollama and self.proc_ollama:
			print('   🔻 Stopping Ollama...', end=' ')
			self.proc_ollama.terminate()
			try:
				self.proc_ollama.wait(timeout=3)
			except subprocess.TimeoutExpired:
				self.proc_ollama.kill()
			print('Done.')
		else:
			print('Ollama left running (External process).')

		print('✅ Session Closed.')