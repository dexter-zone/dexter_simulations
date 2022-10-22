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


        # 
        # return

        VAULT_ADDR = "persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"

        POOL_TYPES = {
            "xyk": {"xyk":{}},
            "Stable2Pool": {"stable2_pool":{}},
            "Stable5Pool": {"stable5_pool":{}},
            "Weighted": {"weighted":{}},
        }

        #------------------------------------------------  VAULT -::- QUERIES  ------------------------------------------------
        #------------------------------------------------  xxxxxxxxxxxxxxxxxx  ------------------------------------------------

        # vault_config = self.query_vault_config(VAULT_ADDR)
        # print(f"\nVAULT Contract Config = {vault_config}")
        
        # vault_registry_xyk = self.query_vault_query_registery(VAULT_ADDR, POOL_TYPES["xyk"]  )
        # print(f"\nVAULT Contract :: Registry :: XYK = {vault_registry_xyk}")

        # vault_registry_xyk = self.query_vault_query_registery(VAULT_ADDR,  POOL_TYPES["Stable2Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-2-Pool = {vault_registry_xyk}")

        # vault_registry_xyk = self.query_vault_query_registery(VAULT_ADDR,  POOL_TYPES["Stable5Pool"]  )
        # print(f"\nVAULT Contract :: Registry :: Stable-5-Pool = {vault_registry_xyk}")

        # vault_registry_xyk = self.query_vault_query_registery(VAULT_ADDR, POOL_TYPES["Weighted"]  )
        # print(f"\nVAULT Contract :: Registry :: Weighted = {vault_registry_xyk}")

        #------------------------------------------------  DEXTER POOLS -::- CREATION  ------------------------------------------------

        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
            { "token": { "contract_addr": "persistence1rtdulljz3dntzpu085c7mzre9dg4trgdddu4tqk7uuuvu6xrfu8s8wcs45" } },
        ]

        # ---xxxx---- Create XYK Pool ---xxxx---
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["xyk"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=None  )
        # # print(create_pool_tx)
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")

        # ---xxxx---- Create Stableswap Pool ---xxxx---- 
        # init_params = self.dict_to_b64({ "amp": 100 })
        # create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Stable2Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        # print(create_pool_tx)
        # self.index_and_store_tx(create_pool_tx, "create_dexter_pool")

        asset_infos = [
            { "native_token": { "denom": "uxprt" } },
            # { "token": { "contract_addr": "persistence1vqpc6fl6v6semp3yhml5mzw8pgcrafawjk5f6cq4723wc47y0l2qualxyh" } }
            { "token": { "contract_addr": "persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq" } },
            { "token": { "contract_addr": "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" } },
        ]

        # res = self.query_token_info("persistence1u2zdjcczjrenwmf57fmrpensk4the84azdm05m3unm387rm8asdsh0yf27")
        # print(res)
        # return

        # ---xxxx----  Create Stable-5-swap Pool ---xxxx---- 
        init_params = self.dict_to_b64({ "amp": 10 })
        create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Stable5Pool"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        print(create_pool_tx)
        self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


        # ---xxxx----  Create Weighted Pool ---xxxx---- 
        init_params = self.dict_to_b64({ "weights": weights, "exit_fee": "0.01", })
        create_pool_tx = self.execute_vault_CreatePoolInstance( VAULT_ADDR, POOL_TYPES["Weighted"], asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=init_params  )
        print(create_pool_tx)
        self.index_and_store_tx(create_pool_tx, "create_dexter_pool")


        # vault_config = self.query_vault_IsGeneratorDisabled(VAULT_ADDR, lp_token_addr)
        # print(f"\nVAULT Contract Config = {vault_config}")

        # vault_config = self.query_vault_GetPoolById(VAULT_ADDR, pool_id)
        # print(f"\nVAULT Contract Config = {vault_config}")

        # vault_config = self.query_vault_GetPoolByAddress(VAULT_ADDR, pool_addr)
        # print(f"\nVAULT Contract Config = {vault_config}")

        # Set generator address in Vault contract
        # update_vault_config_generator_addr_tx = self.execute_vault_UpdateConfig(VAULT_ADDR, None ,None , "persistence12xtk58t59tnv36zcuyzv3lda4emvugcl9y4ar7tavjqzl29dyhgs9039fz")
        # print(update_vault_config_generator_addr_tx)

        # self.get_block_timestamp()
        # return

        # execute_increase_allowance_tx = self.execute_increase_allowance("persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel", "persistence10kkn698hpzm07kj0klhj3hrkxjsmngj9598esypm5kh9hfpealpqpjvhel" ,1)
        # print(execute_increase_allowance_tx)
        # self.index_and_store_tx([execute_increase_allowance_tx])





        # res = self.query_pool_config("persistence1lxansfc8vkujy997e3xksd3ugsppv6a9jt32pjtgaxr0zkcnkznqu22a4s")
        # id_res = self.query_pool_id("persistence1lxansfc8vkujy997e3xksd3ugsppv6a9jt32pjtgaxr0zkcnkznqu22a4s")
        # print(id_res)

        # token_balance = self.query_balance("persistence1vguuxez2h5ekltfj9gjd62fs5k4rl2zy5hfrncasykzw08rezpfst7tmng", self.wallet_addr)
        # print(token_balance)

        # increase_allowance_tx = self.execute_increase_allowance("persistence1vguuxez2h5ekltfj9gjd62fs5k4rl2zy5hfrncasykzw08rezpfst7tmng", VAULT_ADDR, 1000000000)
        # print(increase_allowance_tx)


        # pool_assets = res['assets']
        # print("Pool Assets")
        # for asset in pool_assets:
        #     print(asset["info"])
            # if asset["info"].get("native_token"):
            #     print("Native Token")

        # self.execute_vault_JoinPool(1, None, )
        





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
