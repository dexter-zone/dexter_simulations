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

        self.VAULT_ADDR = "persistence1u5ytk4hvgk33uwa0jqlyjx0rjpsc4xu4m4lv0aem9emf5mtlzejsu2pzc0"
        self.GENERATOR_ADDR = "persistence1n6nvtuv37kevcexhrxns2ukqvut3xmagwfpxezcxtpxfexrzryus9mtdat"
        self.TOKEN_ADDR = [
            {"symbol": "C-LUNC", "contract_addr": "persistence14pca2wuhufwpe4hsuka6ue2fmg0ffl5uumaa4p45l009mjw7r0pqtnz2f5" },
            {"symbol": "C-OSMO", "contract_addr": "persistence1da9krw7mn7cp2p74sus6x0ckfd5c9q5vhqe92yx8cf5dyqu8q8gq7mg5uk" },
            {"symbol": "C-JUNO", "contract_addr": "persistence17ln6t80dtevdwxtat4g3d7gnvn7t6u6lwn9sfl95us4v2ze7uw5qd302s4" },
            {"symbol": "C-JUNO", "contract_addr": "persistence1uakxncqvela43mtpck8azfupk7wzzau8jx785595fc73tqg803hq6mwqqp" },
            {"symbol": "C-JUNO", "contract_addr": "persistence109mcvjd52amnrljjqhhtfp3epza6tw5mmly3ts6jtmuwevvzhvyqz6e4ws" },
            {"symbol": "C-JUNO", "contract_addr": "persistence107sw07mqlgkpysv5mv7m4hgxqcj2elhdhnkrjk5kaeamcfa293tsh4wdl5" },
            {"symbol": "C-JUNO", "contract_addr": "persistence1a544t99uyrc3ewzce0k8gpvlsksnkfn5mcwgq8tpnrwzc73erjgq5p5ak7" },
            {"symbol": "C-JUNO", "contract_addr": "persistence1fkah0lxpjdm746afuw9qvtafvtpgfmvtydg2s5uytzr4fzldh8sq7zexpz" },
            {"symbol": "C-JUNO", "contract_addr": "persistence1cnyksdahdpzkh2wmhpjjg5xwwf6jssgmmxeddwlghd86uu9y8qeqw9hqwg" },
        ]

        self.POOL_TYPES = {
            "xyk": {"xyk":{}},
            "Stable2Pool": {"stable2_pool":{}},
            "Stable5Pool": {"stable5_pool":{}},
            "Weighted": {"weighted":{}},
        }

        # for token in self.TOKEN_ADDR[5:]:
        #     # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        #     increase_allowance_tx = self.execute_increase_allowance(token["contract_addr"],self.VAULT_ADDR, '10000000000000')
        #     # mint_tx = self.execute_mint_tokens(token["contract_addr"], self.wallet_addr,"100000000000000")
        #     # self.index_and_store_tx(mint_tx)   
        #     token_balance = self.query_balance(token["contract_addr"], self.wallet_addr)
        #     print(token_balance)
        # return

        # res = self.query_balance(token_addr, self.wallet_addr)
        # print(res)


        # lp_token_addr = "persistence1zahr4lhn87fwjsytkaykdl9ttdwxsw5we6vg9nav80zm5tyemgasqqu2wk"
        # deposit_for_addr = "persistence1zahr4lhn87fwjsytkaykdl9ttdwxsw5we6vg9nav80zm5tyemgasqqu2wk"
        # deposit_amount = '100'
        # unstake_amount = '10'

        # Initialize a pool in the Generator
        # res = self.execute_generator_SetupPools(self.GENERATOR_ADDR, [(lp_token_addr, '0')] ) 
        # print(res)

        # Add a proxy as allowed to the Generator
        # proxies = [""]
        # set_allowed_reward_proxies_tx = self.execute_generator_set_allowed_reward_proxies(self.GENERATOR_ADDR, proxies)
        # self.index_and_store_tx(set_allowed_reward_proxies_tx)

        # Add or remove a proxy contract that can interact with the Generator
        # add = [""]
        # remove = [""]
        # updateAllowedProxies_tx = self.execute_generator_UpdateAllowedProxies(self.GENERATOR_ADDR, add, remove)
        # self.index_and_store_tx(updateAllowedProxies_tx)

        #  Setup a proxy contract for a specific LP token pool
        # lp_token = ""
        # proxy_addr = ""
        # setupProxyForPool_tx = self.execute_generator_SetupProxyForPool(self.GENERATOR_ADDR, lp_token, proxy_addr)
        # self.index_and_store_tx(setupProxyForPool_tx)



        # Query Generator
        # res = self.query_gen_config(self.GENERATOR_ADDR ) 
        # print(res)
        # return

        # Deposit LP token in Generator Pool
        # deposit_tx = self.execute_generator_Deposit(self.GENERATOR_ADDR, lp_token_addr, deposit_amount)
        # self.index_and_store_tx(deposit_tx)

        # Unstake a token from Generator Pool
        # unstake_tx = self.execute_generator_Unstake(self.GENERATOR_ADDR, lp_token_addr, unstake_amount)
        # self.index_and_store_tx(unstake_tx)

        # Emergency Unstake a token from Generator Pool
        # emerg_unstake_tx = self.execute_generator_EmergencyUnstake(self.GENERATOR_ADDR, lp_token_addr)
        # self.index_and_store_tx(emerg_unstake_tx)

        # Unlocks tokens being unbonded from Generator Pool
        # unlock_tx = self.execute_generator_Unlock(self.GENERATOR_ADDR, lp_token_addr)
        # self.index_and_store_tx(unlock_tx)

        # Claim rewards for the given LP Generator pools 
        # claim_rewards_tx = self.execute_generator_ClaimRewards(self.GENERATOR_ADDR, lp_token_addr)
        # self.index_and_store_tx(claim_rewards_tx)


        # Query tokens deposited in generator for a given pool
        # res = self.query_gen_deposit( self.GENERATOR_ADDR, lp_token_addr, self.wallet_addr )
        # print(res)


        # # Query tokens deposited in generator for a given pool
        # res = self.query_gen_deposit( self.GENERATOR_ADDR, lp_token_addr, self.wallet_addr )
        # print(res)

        # # Query a generator's pool info 
        # res = self.query_gen_PoolInfo( self.GENERATOR_ADDR, lp_token_addr )
        # print(res)

        # # Query user info from the generator for a given pool
        # res = self.query_gen_UserInfo( self.GENERATOR_ADDR, lp_token_addr,  self.wallet_addr)
        # print(res)


        # return




        # Set generator address in Vault contract
        # update_vault_config_generator_addr_tx = self.execute_vault_UpdateConfig( self.VAULT_ADDR, None ,None , self.GENERATOR_ADDR)
        # print(update_vault_config_generator_addr_tx)
        # return

        #------------------------------------------------  VAULT -::- QUERIES  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        # vault_config = self.query_vault_config( self.VAULT_ADDR)
        # print(f"\nVAULT Contract Config = {vault_config}")
        
        # vault_registry = self.query_vault_query_registery( self.VAULT_ADDR, self.POOL_TYPES["xyk"]  )
        # print(f"\nVAULT Contract :: Registry :: XYK = {vault_registry}")

        # vault_registry = self.query_vault_query_registery( self.VAULT_ADDR,  self.POOL_TYPES["Stable2Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-2-Pool = {vault_registry}")

        # vault_registry = self.query_vault_query_registery( self.VAULT_ADDR,  self.POOL_TYPES["Stable5Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-5-Pool = {vault_registry}")

        # vault_registry = self.query_vault_query_registery( self.VAULT_ADDR, self.POOL_TYPES["Weighted"]  )
        # print(f"\nVAULT Contract :: Registry :: Weighted = {vault_registry}")
        # return
        # IsGeneratorDisabled = self.query_vault_IsGeneratorDisabled( self.VAULT_ADDR, "persistence1w4sqzvve7jer3v8pqrwdge7nmwh5k6l6hsd4nzrmksg3ehzcqhjs7ja7zt")
        # print(f"\nVAULT Contract - IsGeneratorDisabled = {IsGeneratorDisabled}")

        # pool_info_by_id = self.query_vault_GetPoolById( self.VAULT_ADDR, '8')
        # print(f"\nVAULT Contract - Query Pool by ID = {pool_info_by_id}")

        # pool_info_by_addr = self.query_vault_GetPoolByAddress( self.VAULT_ADDR, "persistence1w4sqzvve7jer3v8pqrwdge7nmwh5k6l6hsd4nzrmksg3ehzcqhjs7ja7zt")
        # print(f"\nVAULT Contract - Query Pool by addr = {pool_info_by_addr}")


        #------------------------------------------------  TOKENS - Helper queries and functions  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        # token_addr = self.TOKEN_ADDR[0]["contract_addr"]
        # res = self.query_token_info("persistence1x2skrlvnq0cre76zrn0mm9rwefkexszavt5ahrl7qmxxj5xzeluqxultc0")
        # print(res)
        # res = self.query_token_info("persistence1k8pms0ywhsa0kjvkxqx434atqd5dh6w54k0gr8j45ra36q02py5scvqcqd")
        # print(res)
        # res = self.query_token_info("persistence14xsm2wzvu7xaf567r693vgfkhmvfs08l68h4tjj5wjgyn5ky8e2qwd708a")
        # print(res)

        # res = self.query_token_minter("persistence1x2skrlvnq0cre76zrn0mm9rwefkexszavt5ahrl7qmxxj5xzeluqxultc0")
        # print(res)
        # return

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
        # self.simulate_stable5swap_pool()
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
             { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } },
        ]
        pool_id = '1'
        pool_addr = "persistence1nldrmkjqskmpjzkmefmvt4k9xh6rd7z68vf9hggjfnwh5uhgtwrqlsxx0j"
        lp_token_addr = "persistence14ay0q9mpn4qrz9wtc8wyms6pq5lchcynfjn7hskh2u95t4437wmsdnfwv9"

        # ---xxxx---- Create XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---
        # create_pool_tx = self.execute_vault_CreatePoolInstance(self.VAULT_ADDR, self.POOL_TYPES["xyk"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=None  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


        # ---xxxx---- Provide Liquidity XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---
        assets_in = [{ "info":{ "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }, "amount":'1000000000000' }, 
                    {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'1000000000' }]
        slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool(self.VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=1000000000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: XYK Pool ---xxxx--- ---xxxx--- ---xxxx--- ---xxxx---

        swap_request = {
            "pool_id":pool_id,
            "asset_in": { "token": {"contract_addr": self.TOKEN_ADDR[1]["contract_addr"]} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }

        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap(self.VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")

        # ---xxxx---- Remove Liquidity :: XYK Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool(self.VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
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
        # offer_asset = { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }
        # ask_asset = { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance(self.TOKEN_ADDR[1]["contract_addr"],self.VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)

     
    '''
    STABLESWAP Pool
    Functions for executing transactions / querying stableswap Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_stableswap_pool(self):
        
        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } },
        ]
        pool_id = '2'
        pool_addr = "persistence10q9cp39hakhpppjxqe2v0tvl605d9jr9ph4hanluhyfmfxyneqrqasyc36"
        lp_token_addr = "persistence1885yru8hafq7fhmldsdvl09une8x5vzu4a5xpxvt6l7rafwqce8sz4623r"


        # ---xxxx---- Create Stableswap Pool ---xxxx---- 
       
        # init_params = self.dict_to_b64({ "amp": 10 })
        # create_pool_tx = self.execute_vault_CreatePoolInstance(self.VAULT_ADDR, self.POOL_TYPES["Stable2Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")



       # ---xxxx---- Provide Liquidity StableSwap Pool ---xxxx---

        # assets_in = [{ "info":{ "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }, "amount":'1000000000' }, 
        #             {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'1000000000' }]
        # slippage_tolerance = None

        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool(self.VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=1000000000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: StableSwap Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "token": {"contract_addr": self.TOKEN_ADDR[1]["contract_addr"]} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '100',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap(self.VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")

        # ---xxxx---- Remove Liquidity :: StableSwap Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool(self.VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
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
        # offer_asset = { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }
        # ask_asset = { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance(self.TOKEN_ADDR[1]["contract_addr"],self.VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)


     
    '''
    STABLE-5-SWAP Pool
    Functions for executing transactions / querying stable-5-swap Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_stable5swap_pool(self):

        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } },
             { "token": { "contract_addr": self.TOKEN_ADDR[0]["contract_addr"] } },
             { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } },
            #  { "token": { "contract_addr": self.TOKEN_ADDR[3]["contract_addr"] } },
            #  { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } },
        ]


        # ---xxxx----  Create Stable-5-swap Pool ---xxxx---- 

        res = self.query_token_info("persistence1u2zdjcczjrenwmf57fmrpensk4the84azdm05m3unm387rm8asdsh0yf27")
        print(res)

        # init_params = self.dict_to_b64({ "amp": 10 })
        # create_pool_tx = self.execute_vault_CreatePoolInstance( self.VAULT_ADDR, self.POOL_TYPES["Stable5Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


       # ---xxxx---- Provide Liquidity Stable-5-Swap Pool :: Needs to be fixed ---xxxx---

        pool_id = self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["pool_id"]
        pool_addr = self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["pool_addr"]
        lp_token_addr = self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["lp_token_addr"]


        assets_in = [
             { "info":{ "native_token": { "denom": "uxprt" } }, "amount":'1000000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }, "amount":'1000000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[0]["contract_addr"] } }, "amount":'1000000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }, "amount":'1000000000' }, 
            # { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[3]["contract_addr"] } }, "amount":'1000000000' }, 
            # { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }, "amount":'1000000000' }, 
                    ]
        slippage_tolerance = None
        # print(assets_in)
        # provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        # print(provide_liquidity_to_pool_query)

        # provide_liquidity_to_pool_tx = self.execute_vault_JoinPool(self.VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=1000000000)  )
        # self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")


        # ---xxxx---- SWAP Tokens :: Stable-5-Swap Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "token": {"contract_addr": self.TOKEN_ADDR[1]["contract_addr"]} },
            "asset_out":  { "native_token": {"denom": "uxprt"} },
            "swap_type": { "give_in":{} },
            "amount": '10',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap(self.VAULT_ADDR, swap_request,  recipient=None, coins=None  )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")


        # ---xxxx---- Remove Liquidity :: Stable-5-swap Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool(self.VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
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
        # offer_asset = { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }
        # ask_asset = { "token": { "contract_addr": self.TOKEN_ADDR[0]["contract_addr"] } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance(self.TOKEN_ADDR[0]["contract_addr"],self.VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)
        # increase_allowance_tx = self.execute_increase_allowance(self.TOKEN_ADDR[2]["contract_addr"],self.VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)


    '''
    WEIGHTED Pool
    Functions for executing transactions / querying Weighted Pool. 
    TO be used for simulating pool performance
    '''
    def simulate_weighted_pool(self):
        
        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
             { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } },
             { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } },
             { "token": { "contract_addr": self.TOKEN_ADDR[3]["contract_addr"] } },
             { "token": { "contract_addr": self.TOKEN_ADDR[5]["contract_addr"] } },             
             { "token": { "contract_addr": self.TOKEN_ADDR[6]["contract_addr"] } },             
             { "token": { "contract_addr": self.TOKEN_ADDR[7]["contract_addr"] } },             
             { "token": { "contract_addr": self.TOKEN_ADDR[8]["contract_addr"] } }             
        ]

        # ---xxxx----  Create Weighted Pool ---xxxx---- 

        weights = [{ "info": { "native_token": { "denom": "uxprt" } }, "amount": "10" },
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }, "amount": "20",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }, "amount": "30",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[3]["contract_addr"] } }, "amount": "40",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[5]["contract_addr"] } }, "amount": "50",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[6]["contract_addr"] } }, "amount": "40",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[7]["contract_addr"] } }, "amount": "30",},
                   {"info": { "token": { "contract_addr": self.TOKEN_ADDR[8]["contract_addr"] } }, "amount": "20",},
                ]
        # init_params = self.dict_to_b64({ "weights": weights, "exit_fee": "0.005", })
        # create_pool_tx = self.execute_vault_CreatePoolInstance(self.VAULT_ADDR, self.POOL_TYPES["Weighted"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")
        # # return

        pool_id = str(self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["pool_id"])
        pool_addr = self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["pool_addr"]
        lp_token_addr = self.dexter_pools_DF.loc[len(self.dexter_pools_DF)-1]["lp_token_addr"]

       # ---xxxx---- Provide Liquidity WEIGHTED Pool ---xxxx---

        assets_in = [
                    {"info":{ "native_token": {"denom":"uxprt"} }, "amount":'1000000000' },
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }, "amount":'2000000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }, "amount":'300000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[3]["contract_addr"] } }, "amount":'400000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[5]["contract_addr"] } }, "amount":'400000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[6]["contract_addr"] } }, "amount":'400000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[7]["contract_addr"] } }, "amount":'400000000' }, 
            { "info":{ "token": { "contract_addr": self.TOKEN_ADDR[8]["contract_addr"] } }, "amount":'400000000' }, 
                    ]
        slippage_tolerance = None

        provide_liquidity_to_pool_query = self.query_pool_on_join_pool( pool_addr, assets_in, None ,slippage_tolerance )
        print(provide_liquidity_to_pool_query)

        provide_liquidity_to_pool_tx = self.execute_vault_JoinPool(self.VAULT_ADDR, pool_id, recipient=None, assets=assets_in, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins = Coins(uxprt=1000000000)  )
        # print(provide_liquidity_to_pool_tx)
        self.index_and_store_tx(provide_liquidity_to_pool_tx, "provide_liquidity")
        

        # ---xxxx---- SWAP Tokens :: Weighted Pool ---xxxx---

        swap_request = {
            "pool_id": pool_id,
            "asset_in": { "native_token": {"denom": "uxprt"} }, 
            "asset_out":  { "token": {"contract_addr": self.TOKEN_ADDR[1]["contract_addr"]} },
            "swap_type": { "give_in":{} },
            "amount": '10',
            "max_spread": '0.5',
            "belief_price": None
        }
        # swap_via_pool_query = self.query_pool_on_swap( pool_addr, swap_request["swap_type"] ,swap_request["asset_in"],swap_request["asset_out"],swap_request["amount"], swap_request["max_spread"], swap_request["belief_price"] )
        # print(swap_via_pool_query)

        # swap_via_pool_tx = self.execute_vault_Swap(self.VAULT_ADDR, swap_request,  recipient=None, coins= Coins(uxprt=1000000)   )
        # self.index_and_store_tx(swap_via_pool_tx, "swap")


        # ---xxxx---- Remove Liquidity :: Weighted Pool ---xxxx---

        assets_out = None
        burn_amount = '10'

        # remove_liquidity_to_pool_query = self.query_pool_on_exit_pool( pool_addr, assets_out, burn_amount )
        # print(remove_liquidity_to_pool_query)

        # remove_liquidity_to_pool_tx = self.execute_vault_exit_pool(self.VAULT_ADDR, lp_token_addr, burn_amount, pool_id, recipient=None, assets=assets_out, burn_amount=burn_amount  )
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
        # offer_asset = { "token": { "contract_addr": self.TOKEN_ADDR[1]["contract_addr"] } }
        # ask_asset = { "token": { "contract_addr": self.TOKEN_ADDR[2]["contract_addr"] } }
        # res = self.query_cumulative_price(pool_addr, offer_asset, ask_asset)
        # print(res)
        
        # Query Cumulative Prices : Query 
        # res = self.query_cumulative_prices(pool_addr)
        # print(res)

        # INCREASE ALLOWANCE - VAULT CONTRACT needs to be able to transfer tokens from your account when providing liquidity
        # increase_allowance_tx = self.execute_increase_allowance(self.TOKEN_ADDR[1]["contract_addr"],self.VAULT_ADDR, '10000000000000')
        # self.index_and_store_tx(increase_allowance_tx)

    '''
    DEXTER -::- Generator
    '''
    def simulate_generator(self, lp_token_addr, amount):
        deposit_tx = self.execute_generator_Deposit(self.GENERATOR_ADDR, lp_token_addr, amount)
        self.index_and_store_tx(deposit_tx)







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
