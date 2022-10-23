import imp
from cosmos_sdk.client.lcd import LCDClient
from cosmos_sdk.key.mnemonic import MnemonicKey
from cosmos_sdk.core.wasm import  MsgExecuteContract 
from cosmos_sdk.core.fee import Fee
from cosmos_sdk.core import Coins, Coin
from cosmos_sdk.client.lcd.api.tx import CreateTxOptions
import base64
import json



class dexter_helpers_mixin():

    def get_block_timestamp(self):
        block_info = self.client.tendermint.block_info()
        timestamp = block_info["block"]["header"]["time"]
        return timestamp


    def query_token_minter(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"minter":{}})
            return sim_response         
        except:
            return None

    def query_token_info(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"token_info":{}})
            return sim_response         
        except:
            return None

    def execute_mint_tokens(self,contract_addr,recipient, amount ):
        msg = { "mint": {'amount': amount, 'recipient': recipient}}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, contract_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        # tx = self.wallet.create_and_sign_tx( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    ###############################################
    ################ VAULT QUERIES ################
    ###############################################

    def query_vault_config(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"config":{}})
            return sim_response         
        except:
            return None

    def query_vault_query_registery(self,  contract_addr, pool_type):
        try:
            print(pool_type)
            sim_response = self.client.wasm.contract_query(contract_addr , {"query_registry" : { "pool_type": pool_type }})
            return sim_response         
        except:
            return None

    def query_vault_IsGeneratorDisabled(self,  contract_addr, lp_token_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr ,  { "is_generator_disabled" : { "lp_token_addr": lp_token_addr }})
            return sim_response         
        except:
            return None
            
    def query_vault_GetPoolById(self,  contract_addr, pool_id):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr ,  { "get_pool_by_id" : { "pool_id": pool_id }})
            return sim_response         
        except:
            return None

    def query_vault_GetPoolByAddress(self,  contract_addr, pool_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr ,  { "get_pool_by_address" : { "pool_addr": pool_addr }})
            return sim_response         
        except:
            return None


    ###############################################
    ################ POOL QUERIES ################
    ###############################################

    def query_pool_config(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"config":{}})
            return sim_response         
        except:
            return None

    def query_pool_fee_params(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"fee_params":{}})
            return sim_response         
        except:
            return None


    def query_pool_id(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"pool_id":{}})
            return sim_response         
        except:
            return None

    def query_pool_on_join_pool(self,  contract_addr, assets_in=None, mint_amount=None, slippage_tolerance=None):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"on_join_pool":{ 
                "assets_in": assets_in,
                "mint_amount": mint_amount,
                "slippage_tolerance": slippage_tolerance
            }})
            return sim_response         
        except:
            return None

    def query_pool_on_exit_pool(self,  contract_addr, assets_out=None, burn_amount=None):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"on_exit_pool":{ 
                "assets_out": assets_out,
                "burn_amount": burn_amount
            }})
            return sim_response         
        except:
            return None

    def query_pool_on_swap(self,  contract_addr,swap_type,offer_asset,ask_asset,amount, max_spread=None, belief_price=None):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"on_swap":{ 
            "swap_type": swap_type,
            "offer_asset": offer_asset,
            "ask_asset": ask_asset,
            "amount": amount,
            "max_spread": max_spread,
            "belief_price": belief_price,
            }})
            return sim_response         
        except:
            return None


    def query_cumulative_price(self,  contract_addr, offer_asset, ask_asset):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"cumulative_price":{ 
            "offer_asset": offer_asset,
            "ask_asset": ask_asset,
            }})
            return sim_response         
        except:
            return None


    def query_cumulative_prices(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"cumulative_prices":{ 
            }})
            return sim_response         
        except:
            return None


    ###############################################
    ########### CW20 TRANSACTIONS & QUERIES ################
    ###############################################

    def execute_increase_allowance(self,token_addr,spender,amount):
        msg = { "increase_allowance": {'spender': spender,  "amount": amount }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, token_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res


    def query_balance(self,  contract_addr, address):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"balance":{ "address": address}})
            return sim_response         
        except:
            return None

    ###############################################
    ########### VAULT TRANSACTIONS ################
    ###############################################

    def execute_vault_UpdateConfig(self,vault_addr,lp_token_code_id=None,fee_collector=None,generator_address=None ):
        msg = { "update_config": {'lp_token_code_id': lp_token_code_id,  "fee_collector": fee_collector, "generator_address":generator_address  }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        # tx = self.wallet.create_and_sign_tx( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_UpdatePoolConfig(self,vault_addr,pool_type,is_disabled=None,new_fee_info=None ):
        msg = { "update_pool_config": {'pool_type': pool_type,  "is_disabled": is_disabled, "new_fee_info":new_fee_info  }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_AddToRegistery(self,vault_addr,new_pool_config):
        msg = { "add_to_registery": {'new_pool_config': new_pool_config }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_CreatePoolInstance(self,vault_addr, pool_type, asset_infos, lp_token_name=None, lp_token_symbol=None, init_params=None ):
        msg = { "create_pool_instance": {        "pool_type": pool_type,
            "asset_infos": asset_infos,
            "lp_token_name": lp_token_name,
            "lp_token_symbol": lp_token_symbol,
            "init_params": init_params }}
        print(msg)
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_JoinPool(self,vault_addr, pool_id, recipient=None, 
                                assets=None, lp_to_mint=None, slippage_tolerance=None, auto_stake=None, coins=None):
        msg = { "join_pool": {         
            "pool_id": pool_id,
            "recipient": recipient,
            "assets":assets,
            "lp_to_mint": lp_to_mint,
            "slippage_tolerance": slippage_tolerance,
            "auto_stake": auto_stake
             }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg, coins )
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_Swap(self,vault_addr, swap_request, recipient=None, coins=None ):
        msg = { "swap": {         
            "swap_request": swap_request,
            "recipient": recipient }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg, coins)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_ProposeNewOwner(self,vault_addr, owner, expires_in=None ):
        msg = { "propose_new_owner": {         
            owner: owner,
            expires_in: expires_in }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_DropOwnershipProposal(self,vault_addr):
        msg = { "drop_ownership_proposal": {   }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res

    def execute_vault_ClaimOwnership(self,vault_addr):
        msg = { "claim_ownership": {}}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, vault_addr, msg)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res


    def execute_vault_exit_pool(self,vault_addr, lp_token_addr, amount, pool_id,  recipient=None, assets=None, burn_amount=None  ):
        exit_msg = { "exit_pool": {
                    "pool_id": pool_id,
                    "recipient": recipient,
                    "assets": assets,
                    "burn_amount": burn_amount,
                }}
        cw20_send = { "send": {
            "contract": vault_addr,
            "amount" : amount,
            "msg": self.dict_to_b64(exit_msg)
        } }
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, lp_token_addr, cw20_send)
        tx = self.wallet.create_and_sign_tx(CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
        res = self.client.tx.broadcast(tx)
        return res



    ############################################################
    ################ DEXTER GENERATOR - QUERIES ################
    ############################################################

    def query_gen_config(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"config":{  }})
            return sim_response         
        except:
            return None

    # Returns the length of the array that contains all the active pool generators
    def query_gen_ActivePoolLength(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"active_pool_length":{  }})
            return sim_response         
        except:
            return None

    # PoolLength returns the length of the array that contains all the instantiated pool generators
    def query_gen_PoolLength(self,  contract_addr):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"pool_length":{  }})
            return sim_response         
        except:
            return None

    # Deposit returns the LP token amount deposited in a specific generator
    def query_gen_deposit(self,  contract_addr, lp_token, user_addr ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"deposit":{ "lp_token": lp_token, "user": user_addr   }})
            return sim_response         
        except:
            return None

    # PendingToken returns the amount of rewards that can be claimed by an account that deposited a specific LP token in a generator
    def query_gen_pending_token(self,  contract_addr, lp_token, user_addr ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"pending_token":{ "lp_token": lp_token, "user": user_addr   }})
            return sim_response         
        except:
            return None


    # RewardInfo returns reward information for a specified LP token
    def query_gen_RewardInfo(self,  contract_addr, lp_token ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"reward_info":{ "lp_token": lp_token }})
            return sim_response         
        except:
            return None


    # OrphanProxyRewards returns orphaned reward information for the specified LP token
    def query_gen_OrphanProxyRewards(self,  contract_addr, lp_token ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"orphan_proxy_rewards":{ "lp_token": lp_token }})
            return sim_response         
        except:
            return None

    #  PoolInfo returns information about a pool associated with the specified LP token alongside
    #  the total pending amount of DEX and proxy rewards claimable by generator stakers (for that LP token)
    def query_gen_PoolInfo(self,  contract_addr, lp_token ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"pool_info":{ "lp_token": lp_token }})
            return sim_response         
        except:
            return None


    # 
    def query_gen_UserInfo(self,  contract_addr, lp_token, user_addr ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"user_info":{ "lp_token": lp_token, "user": user_addr   }})
            return sim_response         
        except:
            return None


    # SimulateFutureReward returns the amount of DEX that will be distributed until a future block and for a specific generator
    def query_gen_SimulateFutureReward(self,  contract_addr, lp_token, future_block ):
        try:
            sim_response = self.client.wasm.contract_query(contract_addr , {"simulate_future_reward":{ "lp_token": lp_token, "future_block": future_block   }})
            return sim_response         
        except:
            return None

    ######################################################################
    ################ DEXTER GENERATOR - STATE TRANSITIONS ################
    ######################################################################

    # Failitates updating some of the configuration param of the Dexter Generator Contract
    def execute_generator_UpdateConfig(self,generator_addr,dex_token=None,vesting_contract=None,checkpoint_generator_limit=None, unbonding_period=None ):
        msg = { "update_config": {'dex_token': dex_token,  "vesting_contract": vesting_contract, "checkpoint_generator_limit":checkpoint_generator_limit, "unbonding_period":unbonding_period  }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    # Set a new amount of DEX tokens to distribute per block
    def execute_generator_SetTokensPerBlock(self,generator_addr,amount ):
        msg = { "set_tokens_per_block": {'amount': amount}}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    # Setup generators with their respective allocation points.
    def execute_generator_SetupPools(self,generator_addr,pools, ):
        msg = { "setup_pools": {'pools': pools }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    # Failitates updating some of the configuration param of the Dexter Generator Contract
    def execute_generator_SetupProxyForPool(self,generator_addr,lp_token,proxy_addr):
        msg = { "setup_proxy_for_pool": {'lp_token': lp_token,  "proxy_addr": proxy_addr }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    # Allowed reward proxy contracts that can interact with the Generator
    def execute_generator_set_allowed_reward_proxies(self,generator_addr,proxies):
        msg = { "set_allowed_reward_proxies": {'proxies': proxies }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #  Sends orphan proxy rewards (which were left behind after emergency withdrawals) to another address
    def execute_generator_SendOrphanProxyReward(self,generator_addr,recipient, lp_token ):
        msg = { "send_orphan_proxy_reward": { 'recipient':recipient, 'lp_token': lp_token }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res


    #  Add or remove a proxy contract that can interact with the Generator
    def execute_generator_UpdateAllowedProxies(self,generator_addr,add=None, remove=None ):
        msg = { "update_allowed_proxies": { 'add':add, 'remove': remove }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #   Sets the allocation point to zero for the specified pool
    def execute_generator_DeactivatePool(self,generator_addr,lp_token ):
        msg = { "deactivate_pool": { 'lp_token':lp_token }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res


    #    Update rewards and transfer them to user.
    def execute_generator_ClaimRewards(self,generator_addr,lp_tokens ):
        msg = { "claim_rewards": { 'lp_tokens':lp_tokens }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #     Unstake LP tokens from the Generator. LP tokens need to be unbonded for a period of time before they can be withdrawn.
    def execute_generator_Unstake(self,generator_addr,lp_token, amount ):
        msg = { "unstake": { 'lp_token':lp_token, "amount":amount }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #    Unstake LP tokens from the Generator without withdrawing outstanding rewards.  LP tokens need to be unbonded for a period of time before they can be withdrawn.
    def execute_generator_EmergencyUnstake(self,generator_addr,lp_token ):
        msg = { "emergency_unstake": { 'lp_token':lp_token }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #    Unlock and withdraw LP tokens from the Generator
    def execute_generator_Unlock(self,generator_addr,lp_token ):
        msg = { "unlock": { 'lp_token':lp_token }}
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, generator_addr, msg)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #    Deposit performs a token deposit on behalf of the message sender.
    def execute_generator_Deposit(self,generator_addr, lp_token_addr, amount ):
        cw20_send = { "send": {
            "contract": generator_addr,
            "amount" : amount,
            "msg": self.dict_to_b64({ "deposit": { }})
        } }
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, lp_token_addr, cw20_send)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res

    #    Deposit performs a token deposit on behalf of the message sender.
    def execute_generator_DepositFor(self,generator_addr, lp_token_addr, amount, deposit_for_addr ):
        cw20_send = { "send": {
            "contract": generator_addr,
            "amount" : amount,
            "msg": self.dict_to_b64({ "deposit_for": { "beneficiary": deposit_for_addr }})
        } }
        convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, lp_token_addr, cw20_send)
        tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=626250000)),) ) 
        res = self.client.tx.broadcast(tx)
        return res


    ###############################################
    ########### ADMIN FUNCTIONS ################
    ###############################################

    # def execute_increase_allowance(self,token_addr,recepient,amount):
    #     msg = { "increase_allowance": {'recepient': recepient,  "amount": amount }}
    #     convertMsgPrep = MsgExecuteContract(self.wallet.key.acc_address, token_addr, msg)
    #     tx = self.wallet.create_and_sign_tx( CreateTxOptions( msgs=[convertMsgPrep], fee=Fee(5000000, Coins(uxprt=6250000)),) )
    #     res = self.client.tx.broadcast(tx)
    #     print(res)
    #     return res




    def dict_to_b64(self, data: dict) -> str:
        return base64.b64encode(bytes(json.dumps(data), "ascii")).decode()