from setuptools import setup
from zmpe.version import __version__

setup(name='zmpe',
      version=__version__,
      description='The program controls the execution of any programs, scripts or commands OS and sends the execution result to zabbix, and in case of an execution error, it additionally can notify via telegram.',
      long_description_content_type="text/markdown",
      long_description=open('README.md', 'r').read(),
      url='https://github.com/MinistrBob/zabbix-monitoring-programs-execution.git',
      author='Dmitry Bobrovsky',
      author_email='ministrbob777@gmail.com',
      packages=['zmpe'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Monitoring',
      ]
      )
