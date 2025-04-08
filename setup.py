from setuptools import setup, find_packages

setup(
    name='scanner_banco_pro',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'flet>=0.8.0',
    ],
    entry_points={
        'console_scripts': [
            'scanner-banco=scanner_banco.cli:main',
        ],
    },
    author='Marco Aurélio Lima Braganca',
    author_email='m.aurelio877@gmail.com',
    description='Scanner para encontrar acessos inseguros ao banco de dados em código Java.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/10Marco/scanner_banco_pro',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
)
