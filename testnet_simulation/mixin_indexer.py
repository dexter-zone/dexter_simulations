import json


class indexer_helpers_mixin():

    ###############################################
    ################ VAULT QUERIES ################
    ###############################################

    def index_and_store_tx(self, tx, type_ = None):
        indexed_tx = self.index_tx(tx)
        self.store_indexed_tx(indexed_tx)

        if type_ == "create_dexter_pool":
            self.create_pool_indexer_helper(indexed_tx["raw_log"])
        
        elif type_ == "provide_liquidity":
            self.provide_liquidity_indexer_helper(indexed_tx["raw_log"])

        elif type_ == "swap":
            self.swap_indexer_helper(indexed_tx["txhash"], indexed_tx["raw_log"])



    def index_tx(self,  tx_response):    
        return {    
        "timestamp" : tx_response.timestamp,
        "height" : tx_response.height,
        "txhash" : tx_response.txhash,
        "raw_log" : tx_response.raw_log,
        "gas_wanted" : tx_response.gas_wanted,
        "gas_used" : tx_response.gas_used,
        "logs" : tx_response.logs,
        "code" : tx_response.code,
        "codespace" : tx_response.codespace,
        "info" : tx_response.info,
        "data" : tx_response.data,
        }


    def store_indexed_tx(self, indexed_tx_response):
        # get timestamp incase tx failed
        if indexed_tx_response["timestamp"] == None:
            indexed_tx_response["timestamp"] = self.get_block_timestamp()
        # store tx
        self.tx_snapshots_DF = self.tx_snapshots_DF.append(indexed_tx_response, ignore_index= True)
        self.tx_snapshots_DF.to_csv("./data/tx_snapshots.csv", index=False)


    
    def create_pool_indexer_helper(self, rawlog):
        rawlog = json.loads(rawlog)
        pool_info = {
            "pool_id": None,
            "pool_type": None,
            "pool_addr": None,
            "lp_token_addr": None,
            "pool_assets": None,
            "lp_token_name": None,
            "lp_token_symbol": None,
            "total_fee_bps": None,
            "protocol_fee_percent": None,
            "developer_fee_percent": None,
        }

        # Index events related to pool creation
        events = rawlog[0]["events"]
        for event in events:
            # wasm-dexter-pool::set_lp_token
            if event["type"] == "wasm-dexter-pool::set_lp_token":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "lp_token_addr":
                        pool_info["lp_token_addr"] = attr["value"]
            # wasm-dexter-vault::add_pool
            if event["type"] == "wasm-dexter-vault::add_pool":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "pool_assets":
                        pool_info["pool_assets"] = attr["value"]
                    if attr["key"] == "pool_type":
                        pool_info["pool_type"] = attr["value"]
                    if attr["key"] == "pool_id":
                        pool_info["pool_id"] = attr["value"]
                    if attr["key"] == "lp_token_name":
                        pool_info["lp_token_name"] = attr["value"]
                    if attr["key"] == "lp_token_symbol":
                        pool_info["lp_token_symbo"] = attr["value"]
                    if attr["key"] == "total_fee_bps":
                        pool_info["total_fee_bps"] = attr["value"]
                    if attr["key"] == "protocol_fee_percent":
                        pool_info["protocol_fee_percent"] = attr["value"]
                    if attr["key"] == "developer_fee_percent":
                        pool_info["developer_fee_percent"] = attr["value"]
            # wasm-dexter-vault::add_pool_reply
            if event["type"] == "wasm-dexter-vault::add_pool_reply":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "pool_addr":
                        pool_info["pool_addr"] = attr["value"]
                   
        print(pool_info)
        # store tx
        self.dexter_pools_DF = self.dexter_pools_DF.append(pool_info, ignore_index= True)
        self.dexter_pools_DF.to_csv("./data/dexter_pools_DF.csv", index=False)



    def provide_liquidity_indexer_helper(self, rawlog):
        rawlog = json.loads(rawlog)
        pool_info = {
            "block_time_last": None,
            "pool_id": None,
            "lp_tokens_minted": None,
            "provided_assets": None,
            "total_pool_liquidity": None,
        }

        # Index events related to pool creation
        events = rawlog[0]["events"]
        for event in events:
            # wasm-dexter-pool::update-liquidity
            if event["type"] == "wasm-dexter-pool::update-liquidity":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "block_time_last":
                        pool_info["block_time_last"] = attr["value"]
                    if attr["key"] == "pool_assets":
                        pool_info["total_pool_liquidity"] = attr["value"]
                    if attr["key"] == "pool_id":
                        pool_info["pool_id"] = attr["value"]

            # wasm-dexter-vault::join_pool
            if event["type"] == "wasm-dexter-vault::join_pool":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "lp_tokens_minted":
                        pool_info["lp_tokens_minted"] = attr["value"]
                    if attr["key"] == "provided_assets":
                        pool_info["provided_assets"] = attr["value"]
                   
        # store tx
        self.provide_liquidity_txs_DF = self.provide_liquidity_txs_DF.append(pool_info, ignore_index= True)
        self.provide_liquidity_txs_DF.to_csv("./data/provide_liquidity_txs_DF.csv", index=False)


    def swap_indexer_helper(self, txhash, rawlog):
        rawlog = json.loads(rawlog)
        swap_info = {
            "block_time_last": None,
            "txhash": txhash,
            "pool_id": None,
            "offer_asset": None,
            "offer_amount": None,
            "ask_asset": None,
            "ask_amount": None,
            "swap_type" : None,
            "total_fee": None,
            "fee_asset": None,
            "total_pool_liquidity": None,
        }

        # Index events related to pool creation
        events = rawlog[0]["events"]
        for event in events:
            # wasm-dexter-pool::update-liquidity
            if event["type"] == "wasm-dexter-pool::update-liquidity":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "block_time_last":
                        swap_info["block_time_last"] = attr["value"]
                    if attr["key"] == "pool_assets":
                        swap_info["total_pool_liquidity"] = attr["value"]
                    if attr["key"] == "pool_id":
                        swap_info["pool_id"] = attr["value"]

            # wasm-dexter-vault::swap
            if event["type"] == "wasm-dexter-vault::swap":
                attributes = event["attributes"]
                for attr in attributes:
                    if attr["key"] == "swap_type":
                        swap_info["swap_type"] = attr["value"]
                    if attr["key"] == "offer_asset":
                        swap_info["offer_asset"] = attr["value"]
                    if attr["key"] == "offer_amount":
                        swap_info["offer_amount"] = attr["value"]
                    if attr["key"] == "ask_asset":
                        swap_info["ask_asset"] = attr["value"]
                    if attr["key"] == "ask_amount":
                        swap_info["ask_amount"] = attr["value"]
                    if attr["key"] == "fee_asset":
                        swap_info["fee_asset"] = attr["value"]
                    if attr["key"] == "total_fee":
                        swap_info["total_fee"] = attr["value"]
        # store tx
        self.swap_txs_DF = self.swap_txs_DF.append(swap_info, ignore_index= True)
        self.swap_txs_DF.to_csv("./data/swap_txs_DF.csv", index=False)




# [{"events":[{"type":"coin_received","attributes":[{"key":"receiver","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"amount","value":"74uxprt"}]},{"type":"coin_spent","attributes":[{"key":"spender","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"amount","value":"74uxprt"}]},{"type":"execute","attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"_contract_address","value":"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"},{"key":"_contract_address","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"}]},{"type":"message","attributes":[{"key":"action","value":"/cosmwasm.wasm.v1.MsgExecuteContract"},{"key":"module","value":"wasm"},{"key":"sender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]},{"type":"transfer","attributes":[{"key":"recipient","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"sender","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"amount","value":"74uxprt"}]},{"type":"wasm","attributes":[{"key":"_contract_address","value":"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"},{"key":"action","value":"transfer_from"},{"key":"amount","value":"100"},{"key":"by","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"from","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"to","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"}]},{"type":"wasm-dexter-pool::update-liquidity","attributes":[{"key":"_contract_address","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"},{"key":"block_time_last","value":"1666501280"},{"key":"pool_assets","value":"[{\"info\":{\"token\":{\"contract_addr\":\"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq\"}},\"amount\":\"511\"},{\"info\":{\"native_token\":{\"denom\":\"uxprt\"}},\"amount\":\"318\"}]"},{"key":"pool_id","value":"20"},{"key":"vault_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"}]},

# {"type":"wasm-dexter-vault::swap","attributes":[
#     {"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},
#     {"key":"pool_id","value":"20"},
#     {"key":"pool_addr","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"},
#     {"key":"swap_type","value":"give-in"},
#     {"key":"fee_asset","value":"{\"native_token\":{\"denom\":\"uxprt\"}}"},
#     {"key":"total_fee","value":"2"},
#     {"key":"offer_asset","value":"{\"token\":{\"contract_addr\":\"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq\"}}"},
#     {"key":"offer_amount","value":"100"},
#     {"key":"ask_asset","value":"{\"native_token\":{\"denom\":\"uxprt\"}}"},
#     {"key":"ask_amount","value":"74"},
#     {"key":"recipient","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},
#     {"key":"sender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]}]}]





# [{"events":[
#     {"type":"coin_received",
#     "attributes":[{"key":"receiver","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"amount","value":"6250000uxprt"},{"key":"receiver","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"amount","value":"6249999uxprt"}]},
    
#     {"type":"coin_spent",
#     "attributes":[{"key":"spender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"amount","value":"6250000uxprt"},{"key":"spender","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"amount","value":"6249999uxprt"}]},
    
#     {"type":"execute",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"_contract_address","value":"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"},{"key":"_contract_address","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"},{"key":"_contract_address","value":"persistence1dy4gx3tpesmnp3kyrra5qukns48cgg9lc8zkzfn3z9aq6d9v0uaqpz4mu6"}]},
    
#     {"type":"message",
#     "attributes":[{"key":"action","value":"/cosmwasm.wasm.v1.MsgExecuteContract"},{"key":"module","value":"wasm"},{"key":"sender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]},
    
#     {"type":"transfer",
#     "attributes":[{"key":"recipient","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"sender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"amount","value":"6250000uxprt"},{"key":"recipient","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"sender","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"amount","value":"6249999uxprt"}]},
    
#     {"type":"wasm",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"action","value":"dexter-vault/execute/join_pool"},{"key":"_contract_address","value":"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq"},{"key":"action","value":"transfer_from"},{"key":"amount","value":"1"},{"key":"by","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"from","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"},{"key":"to","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"_contract_address","value":"persistence1dy4gx3tpesmnp3kyrra5qukns48cgg9lc8zkzfn3z9aq6d9v0uaqpz4mu6"},{"key":"action","value":"mint"},{"key":"amount","value":"1"},{"key":"to","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]},
    
#     {"type":"wasm-dexter-pool::update-liquidity",
#     "attributes":[{"key":"_contract_address","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"},
#                     {"key":"block_time_last","value":"1666444386"},
#                     {"key":"pool_assets","value":"[{\"info\":{\"token\":{\"contract_addr\":\"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq\"}},\"amount\":\"1\"},{\"info\":{\"native_token\":{\"denom\":\"uxprt\"}},\"amount\":\"1\"}]"},
#                     {"key":"pool_id","value":"20"},
#                     {"key":"vault_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"}]},
    
#     {"type":"wasm-dexter-vault::join_pool",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},
#                     {"key":"pool_id","value":"20"},
#                     {"key":"pool_addr","value":"persistence1skpqtmc6n8kg3ksu7734kxtzezhlckgcq30fs44qt40w9h8njqyq4f0fpa"},
#                     {"key":"lp_tokens_minted","value":"1"},
#                     {"key":"provided_assets","value":"[{\"info\":{\"token\":{\"contract_addr\":\"persistence1ekc95e6p7277t77ahxn2dhl5qz76r6egdlrdp2ehvewdraa97m7qfz2ydq\"}},\"amount\":\"1\"},{\"info\":{\"native_token\":{\"denom\":\"uxprt\"}},\"amount\":\"1\"}]"},
#                     {"key":"recipient","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]}]}]

















# [ {"events":
# [  
#     { "type":"execute",
#     "attributes":[ {"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"_contract_address","value":"persistence1dglg47995fhw79pgr4lp0evjpp7uxeuq9mvtrmaf7hl3j00n20xsgue4dl"}]},

#     {"type":"instantiate",
#     "attributes":[{"key":"_contract_address","value":"persistence1dglg47995fhw79pgr4lp0evjpp7uxeuq9mvtrmaf7hl3j00n20xsgue4dl"},{"key":"code_id","value":"26"},{"key":"_contract_address","value":"persistence1ptgs78khanfuzjldx4q0880ksf33ty29q0mw7650mhtnyhyxyq6smn7a8p"},{"key":"code_id","value":"25"}]},
    
#     {"type":"message",
#     "attributes":[{"key":"action","value":"/cosmwasm.wasm.v1.MsgExecuteContract"},{"key":"module","value":"wasm"},{"key":"sender","value":"persistence1pss7nxeh3f9md2vuxku8q99femnwdjtcpe9ky9"}]},
    
#     {"type":"reply",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"}]},
    
#     {"type":"wasm",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"action","value":"reply"},{"key":"pool_addr","value":"persistence1dglg47995fhw79pgr4lp0evjpp7uxeuq9mvtrmaf7hl3j00n20xsgue4dl"},{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},{"key":"action","value":"reply"},{"key":"lp_token_addr","value":"persistence1ptgs78khanfuzjldx4q0880ksf33ty29q0mw7650mhtnyhyxyq6smn7a8p"}]},
    
#     {"type":"wasm-dexter-pool::set_lp_token",
#     "attributes":[{"key":"_contract_address","value":"persistence1dglg47995fhw79pgr4lp0evjpp7uxeuq9mvtrmaf7hl3j00n20xsgue4dl"},
#                     {"key":"lp_token_addr","value":"persistence1ptgs78khanfuzjldx4q0880ksf33ty29q0mw7650mhtnyhyxyq6smn7a8p"}]},
    
#     {"type":"wasm-dexter-vault::add_pool",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},
#                     {"key":"pool_assets","value":"[{\"info\":{\"token\":{\"contract_addr\":\"persistence1u2zdjcczjrenwmf57fmrpensk4the84azdm05m3unm387rm8asdsh0yf27\"}},\"amount\":\"0\"},{\"info\":{\"native_token\":{\"denom\":\"uxprt\"}},\"amount\":\"0\"}]"},
#                     {"key":"pool_type","value":"xyk"},
#                     {"key":"pool_id","value":"5"},
#                     {"key":"lp_token_name","value":"5-Dex-LP"},
#                     {"key":"lp_token_symbol","value":"DEX-LP"},
#                     {"key":"total_fee_bps","value":"300"},
#                     {"key":"protocol_fee_percent","value":"49"},
#                     {"key":"developer_fee_percent","value":"15"}]},
    
#     {"type":"wasm-dexter-vault::add_pool_reply",
#     "attributes":[{"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},
#                     {"key":"pool_id","value":"5"},
#                     {"key":"pool_addr","value":"persistence1dglg47995fhw79pgr4lp0evjpp7uxeuq9mvtrmaf7hl3j00n20xsgue4dl"},
#                     {"key":"_contract_address","value":"persistence1wqchrjh07e3kxaee59yrpzckwr94j03zchmdslypvkv6ps0684ms3yd9xx"},
#                     {"key":"lp_token_addr","value":"persistence1ptgs78khanfuzjldx4q0880ksf33ty29q0mw7650mhtnyhyxyq6smn7a8p"}]}
# ]}
# ]

