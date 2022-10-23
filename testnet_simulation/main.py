# from model import DexterModel
import asyncio
from cosmos_sdk.client.lcd import LCDClient
from cosmos_sdk.key.mnemonic import MnemonicKey
from cosmos_sdk.core.wasm import  MsgExecuteContract 
from cosmos_sdk.core.fee import Fee
from cosmos_sdk.core import Coins, Coin
import pandas as pd


from config import CHAIN_ID, LCD_URL
from mixin_dexter_helper import dexter_helpers_mixin
from mixin_indexer import indexer_helpers_mixin

class DexterModel(dexter_helpers_mixin, indexer_helpers_mixin):

    def __init__(self):

        mnemonic = "opinion knife other balcony surge more bamboo canoe romance ask argue teach anxiety adjust spike mystery wolf alone torch tail six decide wash alley"

        self.client = LCDClient(chain_id=CHAIN_ID, url=LCD_URL)
        self.wallet = self.client.wallet(MnemonicKey(mnemonic,"persistence"))

        block_num = self.client.tendermint.block_info()['block']['header']['height']
        self.wallet_addr = self.wallet.key.acc_address
        print(f"Wallet address = {self.wallet_addr} || Block number = {block_num}")

        # Tx Snapshots DF
        try:
            self.tx_snapshots_DF = pd.read_csv ("./data/tx_snapshots.csv")
        except:
            self.tx_snapshots_DF = pd.DataFrame([], columns = ['timestamp', 'height', 'txhash', 'raw_log' ,'gas_wanted', 'gas_used' , 'logs', 'code', 'codespace' , 'info','data'])


        # Dexter Pools List DF
        try:
            self.dexter_pools_DF = pd.read_csv ("./data/dexter_pools_DF.csv")
        except:
            self.dexter_pools_DF = pd.DataFrame([], columns = ['pool_id', 'pool_type', 'pool_addr', 'lp_token_addr' ,'pool_assets', 'lp_token_name' , 'lp_token_symbol', 'total_fee_bps', 'protocol_fee_percent' , 'developer_fee_percent'])


        # Provide Liquidity Txs List DF
        try:
            self.provide_liquidity_txs_DF = pd.read_csv ("./data/provide_liquidity_txs_DF.csv")
        except:
            self.provide_liquidity_txs_DF = pd.DataFrame([], columns = ['block_time_last','pool_id', 'lp_tokens_minted', 'provided_assets', 'total_pool_liquidity'])

        # Swap Txs List DF
        try:
            self.swap_txs_DF = pd.read_csv ("./data/swap_txs_DF.csv")
        except:
            self.swap_txs_DF = pd.DataFrame([], columns = ['block_time_last','txhash', 'pool_id', 'offer_asset', 'offer_amount', 'ask_asset', 'ask_amount', 'swap_type', 'total_fee', 'fee_asset', 'total_pool_liquidity' ])

        # Remove Liquidity Txs List DF
        try:
            self.remove_liquidity_txs_DF = pd.read_csv ("./data/remove_liquidity_txs_DF.csv")
        except:
            self.remove_liquidity_txs_DF = pd.DataFrame([], columns = ['block_time_last','txhash', 'pool_id', 'pool_addr', 'lp_tokens_burnt', 'assets_out', 'recipient_addr' ])


        # 
        # return

        VAULT_ADDR = "persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"
        TOKEN_ADDR = [
            {},
            {"symbol": "C-LUNC", "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"},
            {"symbol": "C-OSMO", "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel"},
            {"symbol": "C-JUNO", "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh"},
        ]

        POOL_TYPES = {
            "xyk": {"xyk":{}},
            "Stable2Pool": {"stable2_pool":{}},
            "Stable5Pool": {"stable5_pool":{}},
            "Weighted": {"weighted":{}},
        }

        # Set generator address in Vault contract
        # update_vault_config_generator_addr_tx = self.execute_vault_UpdateConfig(VAULT_ADDR, None ,None , "persistence12xtk58t59tnv36zcuyzv3lda4emvugcl9y4ar7tavjqzl29dyhgs9039fz")
        # print(update_vault_config_generator_addr_tx)

        #------------------------------------------------  VAULT -::- QUERIES  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        # vault_config = self.query_vault_config(VAULT_ADDR)
        # print(f"\nVAULT Contract Config = {vault_config}")
        
        # vault_registry = self.query_vault_query_registery(VAULT_ADDR, POOL_TYPES["xyk"]  )
        # print(f"\nVAULT Contract :: Registry :: XYK = {vault_registry}")

        # vault_registry = self.query_vault_query_registery(VAULT_ADDR,  POOL_TYPES["Stable2Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-2-Pool = {vault_registry}")

        # vault_registry = self.query_vault_query_registery(VAULT_ADDR,  POOL_TYPES["Stable5Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-5-Pool = {vault_registry}")

        # vault_registry = self.query_vault_query_registery(VAULT_ADDR, POOL_TYPES["Weighted"]  )
        # print(f"\nVAULT Contract :: Registry :: Weighted = {vault_registry}")

        # IsGeneratorDisabled = self.query_vault_IsGeneratorDisabled(VAULT_ADDR, "persistence1w4sqzvve7jer3v8pqrwdge7nmwh5k6l6hsd4nzrmksg3ehzcqhjs7ja7zt")
        # print(f"\nVAULT Contract - IsGeneratorDisabled = {IsGeneratorDisabled}")

        # pool_info_by_id = self.query_vault_GetPoolById(VAULT_ADDR, '18')
        # print(f"\nVAULT Contract - Query Pool by ID = {pool_info_by_id}")

        # pool_info_by_addr = self.query_vault_GetPoolByAddress(VAULT_ADDR, "persistence1w4sqzvve7jer3v8pqrwdge7nmwh5k6l6hsd4nzrmksg3ehzcqhjs7ja7zt")
        # print(f"\nVAULT Contract - Query Pool by addr = {pool_info_by_addr}")


        #------------------------------------------------  TOKENS - Helper queries and functions  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        # token_addr = "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh"
        # res = self.query_token_info(token_addr)
        # print(res)

        # res = self.query_token_minter(token_addr)
        # print(res)

        # tx = self.execute_mint_tokens(token_addr, self.wallet_addr,"100000000000000")
        # print(tx)
        # self.index_and_store_tx(tx)

        # res = self.query_balance(token_addr, self.wallet_addr)
        # print(res)

        # token_balance = self.query_balance("persistence1vguuxez2h5ekltfj9gjd62fs5k4rl2zy5hfrncasykzw08rezpfst7tmng", self.wallet_addr)
        # print(token_balance)

        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        self.simulate_xyk_pool()
        self.simulate_stableswap_pool()
        self.simulate_stable5swap_pool()
        self.simulate_weighted_pool()
        
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------


        # ---xxxx---- DEXTER -::- Generator Txs ---xxxx---





        
    '''
    XYK Pool
    Functions for executing transactions / querying XYK Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_xyk_pool(self):

        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } },
        ]
        pool_id = '20'
        pool_addr = "persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"
        lp_token_addr = "persistence1dy4gx3tpesmnp3kyrra5qukns48cgg9lc8zkzfn3z9aq6d9v0uaqpz4mu6"

        # ---xxxx---- Create XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["xyk"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=None  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


        # ---xxxx---- Provide Liquidity XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---
        assets_in = [{ "info":{ "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }, "amount":'100' }, 
                    {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'100' }]
        slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool( VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=6250000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        swap_request = {
            "pool_id":pool_id,
            "asset_in": { "token": {"contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }

        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap( VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")

        # ---xxxx---- Remove Liquidity :: XYK Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool( VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
        # self.index_and_store_tx(remove_liquidity_to_pool_tx, "remove_liquidity")

        # ---xxxx---- QUERY AND RELATED HELPERS ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        # Query Pool Config : Query 
        # res = self.query_pool_config(pool_addr)
        # print(res)

        # Query Fee params : Query 
        # res = self.query_pool_fee_params(pool_addr)
        # print(res)

        # Query Pool Id : Query 
        # res = self.query_pool_id(pool_addr)
        # print(res)

        # Query Cumulative Price for token : Query 
        # offer_asset = { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }
        # ask_asset = { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance("persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq", VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)

     
    '''
    STABLESWAP Pool
    Functions for executing transactions / querying stableswap Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_stableswap_pool(self):
        
        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } },
        ]
        pool_id = '21'
        pool_addr = "persistence17rkj7w3d3v0lgutanxcmczah3ls7qwphp5y48574ae3882tgvmequmhu9r"
        lp_token_addr = "persistence16jg37axpyr7wwqjmm5mhnvzxh4xjfguy0u7zhc0382scepd9jugshc7ndp"


        # ---xxxx---- Create Stableswap Pool ---xxxx---- 
       
        # init_params = self.dict_to_b64({ "amp": 10 })
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Stable2Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")



       # ---xxxx---- Provide Liquidity StableSwap Pool ---xxxx---

        assets_in = [{ "info":{ "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }, "amount":'100' }, 
                    {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'1000' }]
        slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool( VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=6250000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: StableSwap Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "token": {"contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap( VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")

        # ---xxxx---- Remove Liquidity :: StableSwap Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool( VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
        # self.index_and_store_tx(remove_liquidity_to_pool_tx, "remove_liquidity")

        # ---xxxx---- QUERY AND RELATED HELPERS ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        # Query Pool Config : Query 
        # res = self.query_pool_config(pool_addr)
        # print(res)

        # Query Fee params : Query 
        # res = self.query_pool_fee_params(pool_addr)
        # print(res)

        # Query Pool Id : Query 
        # res = self.query_pool_id(pool_addr)
        # print(res)

        # Query Cumulative Price for token : Query 
        # offer_asset = { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }
        # ask_asset = { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance("persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq", VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)


     
    '''
    STABLE-5-SWAP Pool
    Functions for executing transactions / querying stable-5-swap Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_stable5swap_pool(self):

        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } },
             { "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } },
             { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } },
        ]
        pool_id = '27'
        pool_addr = "persistence1lqndudd7z6vafksxel5qkuyrzakm4l9mpnkn73579kyh46aelttsqtrugs"
        lp_token_addr = "persistence1dy4gx3tpesmnp3kyrra5qukns48cgg9lc8zkzfn3z9aq6d9v0uaqpz4mu6"


        # ---xxxx----  Create Stable-5-swap Pool ---xxxx---- 

        # res = self.query_token_info("persistence1u2zdjcczjrenwmf57fmrpensk4the84azdm05m3unm387rm8asdsh0yf27")
        # print(res)

        init_params = self.dict_to_b64({ "amp": 10 })
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Stable5Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


       # ---xxxx---- Provide Liquidity Stable-5-Swap Pool :: Needs to be fixed ---xxxx---

        assets_in = [
            { "info":{ "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }, "amount":'100' }, 
            { "info":{ "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }, "amount":'100' }, 
            { "info":{ "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } }, "amount":'100' }, 
                    ]
        slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool( VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=6250000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: Stable-5-Swap Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "token": {"contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap( VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")


        # ---xxxx---- Remove Liquidity :: Stable-5-swap Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool( VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
        # self.index_and_store_tx(remove_liquidity_to_pool_tx, "remove_liquidity")

        # ---xxxx---- QUERY AND RELATED HELPERS ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        # Query Pool Config : Query 
        # res = self.query_pool_config(pool_addr)
        # print(res)

        # Query Fee params : Query 
        # res = self.query_pool_fee_params(pool_addr)
        # print(res)

        # Query Pool Id : Query 
        # res = self.query_pool_id(pool_addr)
        # print(res)

        # Query Cumulative Price for token : Query 
        # offer_asset = { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }
        # ask_asset = { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance("persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq", VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)


    '''
    WEIGHTED Pool
    Functions for executing transactions / querying Weighted Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_weighted_pool(self):
        
        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } },
             { "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } },
             { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } },
        ]
        pool_id = '28'
        pool_addr = "persistence189y9w6tj56g72ud8vjce0vfnkse6v7rp3jjuqkavugnwgduqqj7qzjsh3g"
        lp_token_addr = "persistence1dy4gx3tpesmnp3kyrra5qukns48cgg9lc8zkzfn3z9aq6d9v0uaqpz4mu6"

        # ---xxxx----  Create Weighted Pool ---xxxx---- 

        weights = [{ "info": { "native_token": { "denom": "uxprt" } }, "amount": "10" },
                   {"info": { "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } }, "amount": "20",},
                   {"info": { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }, "amount": "30",},
                   {"info": { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }, "amount": "40",},
                ]
        init_params = self.dict_to_b64({ "weights": weights, "exit_fee": "0.005", })
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Weighted"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


       # ---xxxx---- Provide Liquidity WEIGHTED Pool ---xxxx---

        assets_in = [
            { "info":{ "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }, "amount":'100' }, 
            { "info":{ "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }, "amount":'100' }, 
            { "info":{ "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } }, "amount":'100' }, 
                    {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'1000' }
                    ]
        slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool( VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=6250000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")
        

        # ---xxxx---- SWAP Tokens :: Weighted Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "token": {"contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap( VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")


        # ---xxxx---- Remove Liquidity :: Weighted Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool( VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
        # print(remove_liquidity_to_pool_tx)
        # self.index_and_store_tx(remove_liquidity_to_pool_tx, "remove_liquidity")

        # ---xxxx---- QUERY AND RELATED HELPERS ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        # Query Pool Config : Query 
        # res = self.query_pool_config(pool_addr)
        # print(res)

        # Query Fee params : Query 
        # res = self.query_pool_fee_params(pool_addr)
        # print(res)

        # Query Pool Id : Query 
        # res = self.query_pool_id(pool_addr)
        # print(res)

        # Query Cumulative Price for token : Query 
        # offer_asset = { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } }
        # ask_asset = { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance("persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq", VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)








def execute_simulation():
        dexter_simulation = DexterModel()
        i = 0

        # dexter_simulation.update_agents_state()

        # while i < 10000: 
        #     await dexter_simulation.step()
        #     i = i + 1




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    execute_simulation()
    loop.close()

    # while(1):
    #     try:
    #         loop.run_until_complete(execute_simulation())
    #     except Exception as e:
    #         print(e)  
    #         if e == KeyboardInterrupt:
    #             break
    #         # pass

    # asyncio.sleep(59*59)
