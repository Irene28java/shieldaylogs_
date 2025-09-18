
from setuptools import setup, find_packages

setup(
    name='shieldai_logs',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        
    ],
    python_requires='>=3.10',
    description='Libreria IA para analizar logs y detectar anomalías en seguridad',
    author='Irene Vaquerizo',
    url='https://github.com/irene_java28/shieldai_logs'
)