###########
import argparse
import os

class EnvDefault(argparse.Action):
	def __init__(self, envvar, required=True, default=None, **kwargs):
		if envvar and envvar in os.environ:
			default = os.environ[envvar]
		if required and default is not None:
			required = False
		super(EnvDefault, self).__init__(default=default, required=required,
										 **kwargs)

	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, values)
###########
