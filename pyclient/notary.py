#!/usr/bin/env python3

'''
Command line interface for notary TF.
Parses command line arguments and passes to the NotaryClient class
to process.
'''

import argparse
import logging
import os
import sys
import traceback

from colorlog import ColoredFormatter
from notary_client import NotaryClient

KEY_NAME = 'mynotary'

# hard-coded for simplicity (otherwise get the URL from the args in main):
#DEFAULT_URL = 'http://localhost:8008'
# For Docker:
DEFAULT_URL = 'http://rest-api:8008'

def create_console_handler(verbose_level):
    '''Setup console logging.'''
    del verbose_level # unused
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)
    clog.setLevel(logging.DEBUG)
    return clog

def setup_loggers(verbose_level):
    '''Setup logging.'''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))

def _get_private_keyfile(key_name):
    '''Get the private key for key_name.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, key_name)

def do_sale(buyer, seller, houseinfo):
    '''Calls client class to record sale.'''
    privkeyfile = _get_private_keyfile(KEY_NAME)
    client = NotaryClient(base_url=DEFAULT_URL, key_file=privkeyfile)
    response = client.sale(buyer, seller, houseinfo)
    print("Sale transaction response: {}".format(response))

def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    '''Entry point function for the client CLI.'''
    buyer = input("Buyer name: ")
    seller = input("Seller name: ")
    house = input("House ID: ")
    verbose_level = 0
    setup_loggers(verbose_level=verbose_level)
    # Get the commands from cli args and call corresponding handlers
    do_sale(buyer, seller, house)

if __name__ == '__main__':
    main()
#DOCKER CONTAINER
