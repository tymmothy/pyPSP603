from distutils.core import setup
setup(name='psp603',
      version='0.1',
      author='Tymm Twillman',
      author_email='tymmothy@gmail.com',
      description='GW-Instek PSP603 power supply control module',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
      ],
      license='BSD-new',
      requires=[
          'pySerial',
      ],
      provides=[
          'psp603',
      ],
      py_modules=['psp603'],
      )

