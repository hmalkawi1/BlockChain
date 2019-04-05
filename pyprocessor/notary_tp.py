#!/usr/bin/env python3

import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

# hard-coded for simplicity (otherwise get the URL from the args in main):
#DEFAULT_URL = 'tcp://localhost:4004'
# For Docker:
DEFAULT_URL = 'tcp://validator:4004'

LOGGER = logging.getLogger(__name__)

FAMILY_NAME = "notary"
# TF Prefix is first 6 characters of SHA-512("notary"), !a4d219
#                                                     =  58504b5

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

def _get_notary_address(from_key):
    '''
    Return the address of a notary object from the notary TF.

    The address is the first 6 hex characters from the hash SHA-512(TF name),
    plus the result of the hash SHA-512(notary public key).
    '''
    return _hash(FAMILY_NAME.encode('utf-8'))[0:6] + \
                 _hash(from_key.encode('utf-8'))[0:64]


class NotaryTransactionHandler(TransactionHandler):
    '''
    Transaction Processor class for the notary Transaction Family.

    This TP communicates with the Validator using the accept/get/set functions.
    '''
    def __init__(self, namespace_prefix):
        '''Initialize the transaction handler class.

           This is setting the "notary" TF namespace prefix.
        '''
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        '''Return Transaction Family name string.'''
        return FAMILY_NAME

    @property
    def family_versions(self):
        '''Return Transaction Family version string.'''
        return ['1.0']

    @property
    def namespaces(self):
        '''Return Transaction Family namespace 6-character prefix.'''
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        '''This implements the apply function for the TransactionHandler class.

           The apply function does most of the work for this class by
           processing a transaction for the notary transaction family.
        '''

        # Get the payload and extract the notary-specific information.
        # It has already been converted from Base64, but needs deserializing.
        # It was serialized with CSV: action, value
        #                       Actually buyer name, seller name, Houseid
        header = transaction.header
        payload_list = transaction.payload.decode().split("{")
        buyer_name = payload_list[0]
        seller_name = payload_list[1]
        house_id = payload_list[2]

        # Get the signer's public key, sent in the header from the client.
        from_key = header.signer_public_key
        # Perform the action.
        LOGGER.info("Buyer = %s.", buyer_name)
        LOGGER.info("Seller = %s.", seller_name)
        LOGGER.info("House = %s.", house_id)

        stringdata = '{' + buyer_name + seller_name + house_id + '}'
        self._make_sale(context, stringdata, from_key)
        

    @classmethod
    def _make_sale(cls, context, stringdata, from_key):
        notary_address = _get_notary_address(from_key)
        LOGGER.info('Recieved the key %s and the notary address %s.',
                    from_key, notary_address)
        state_entries = context.get_state([notary_address])
        new_sales = ''

        if state_entries == []:
            LOGGER.info('First sale')
            new_sales = stringdata
        else:
            try:
                sales = str(state_entries[0].data)
            except:
                raise InternalError('Failed to load state data')
            new_sales = str(stringdata) + str(sales)

        state_data = str(new_sales).encode('utf-8')
        addresses = context.set_state({notary_address: state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")
        context.add_event(
            event_type="notary/add",
            attributes=[("sale-added", stringdata)])

def main():
    '''Entry-point function for the notary Transaction Processor.'''
    try:
        # Setup logging for this class.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

        # Register the Transaction Handler and start it.
        processor = TransactionProcessor(url=DEFAULT_URL)
        sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]
        handler = NotaryTransactionHandler(sw_namespace)
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
