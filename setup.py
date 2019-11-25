from setuptools import setup
setup(
    name='php_doc_gen',
    version='1',
    packages=['php_doc_gen'],
    url='',
    license='',
    author='User',
    author_email='',
    description='',
    entry_points={
        'console_scripts': [
            'php_doc_gen = php_doc_gen.__main__:main'
        ]
    },
    install_requires=['bs4']
)
