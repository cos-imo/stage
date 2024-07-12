import sys
import argparse
import ctypes
import os
import subprocess
from pathlib import Path

from tabulate import tabulate

from hypothesis import given
from hypothesis.strategies import text 

class Parseur:
    def __init__(self):
        self.parser = argparse.ArgumentParser(usage='python3 alzette.py [OPTIONS]', add_help=False, description='Python script to launch a Jasmins\' implementation of Alzette')
        self.parse_arguments()

    def parse_arguments(self):
        self.parser.add_argument('-h', '--help', action='help', help="shows this help message")
        self.parser.add_argument('-p', '--program', type=str, help='functions to summon. Choices: crax_export, esch_export, schwaemm_export, sparkle384_11_export, sparkle384_7_export')

        self.args = self.parser.parse_args()

class Wrapper:

	def __init__(self):
		int32 = ctypes.c_int32
		int64 = ctypes.c_int64

		self.args = {"alzette_export": [int32, int32, int32],"crax_export": [int32, int32, int32, int32, int32, int32], "esch_export" : [int64, int32]}

		self.loadlibraries()

		# "schwaemm_export" : [int64, int256, int64, int64, int64], -> pas de u256 dans ctypes? 

		self.parseur = Parseur()
		self.set_func(self.parseur.args.program)

	def loadlibraries(self):
		self.try_load_library()

	def try_load_library(self):
		if Path(f"../shared/sparkle_suite.so").exists():
			self.load_library()
			return
		else:
			sys.stdout.write(f"Jasmin sparkle suite library (.so) not found. Please compile it.\nExiting\n")
			exit()

	def load_library(self):
		self.library = ctypes.cdll.LoadLibrary("../shared/sparkle_suite.so")

	def set_func(self, function):
		func = getattr(self.library, function)
		func.argtypes = self.args[function]
		#self.jasmin_sparkle_dll.crax_export.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64]
		"""
		if function not in ["crax_export", "esch_export", "schwaemm_export", "sparkle384_11_export", "schwaemm384_7_export"]:
			print("function not recognized")
			print("Available functions:")
			for key in self.args:
				print(f"\t* {key}")
		else:
			func = getattr(self.jasmin_sparkle_dll, function)
			func.args = self.args[function]
        """

if __name__ == "__main__":
	wrapper = Wrapper()
