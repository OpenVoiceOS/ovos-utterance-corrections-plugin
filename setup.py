#!/usr/bin/env python3
import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'ovos_utterance_corrections_transformer', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


UTTERANCE_ENTRY_POINT = (
    'ovos-utterance-corrections-plugin=ovos_utterance_corrections_transformer:UtteranceCorrectionsPlugin'
)


setup(
    name='ovos-utterance-corrections-plugin',
    version=get_version(),
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    url='https://github.com/OpenVoiceOS/ovos-utterance-corrections-plugin',
    license='apache-2.0',
    packages=['ovos_utterance_corrections_transformer'],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'neon.plugin.text': UTTERANCE_ENTRY_POINT
    }
)