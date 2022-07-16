import time
import unittest

import near_api
from config import NODE_URL, TEST_ACCOUNT, TEST_KEY_PAIR
from utils import create_account


class JsonProviderTest(unittest.TestCase):
    def setUp(self):
        self.provider = near_api.providers.JsonProvider(NODE_URL)
        self.signer = near_api.signer.Signer(
            TEST_ACCOUNT,
            near_api.signer.KeyPair(TEST_KEY_PAIR)
        )
        self.master_account = near_api.account.Account(self.provider, self.signer)

    def test_status(self):
        status = self.provider.get_status()
        self.assertIsNotNone(status["chain_id"])

    def test_get_account(self):
        response = self.provider.get_account(TEST_ACCOUNT)
        self.assertEqual(response["code_hash"], "11111111111111111111111111111111")

    def test_get_validators_orders(self):
        status = self.provider.get_status()
        latest_block_hash = status['sync_info']['latest_block_hash']
        self.assertEqual(
            self.provider.get_validators_ordered(latest_block_hash)[0]
            ['account_id'],
            TEST_ACCOUNT
        )

    def test_get_next_light_client_block(self):
        status = self.provider.get_status()
        latest_block_hash = status['sync_info']['latest_block_hash']
        receiver = create_account(self.master_account)
        result = self.master_account.send_money(receiver.account_id, 1000)
        time.sleep(3)
        next_light_client_block = self.provider.get_next_light_client_block(latest_block_hash)
        self.provider.get_light_client_proof(
            'transaction', result['transaction']['hash'],
            result['transaction']['receiver_id'],
            next_light_client_block['prev_block_hash']
        )
