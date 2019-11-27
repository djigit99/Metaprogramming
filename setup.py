from setuptools import setup
setup(
    name='php_doc_gen',
    version='1.0',
    packages=['php_doc_gen'],
    url='',
    license='',
    author='Andrii Perun',
    author_email='andrewfreelan@gmail.com',
    description='PHP Documentation Generator',
    entry_points={
        'console_scripts': [
            'php_doc_gen = php_doc_gen.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=['bs4']
)
