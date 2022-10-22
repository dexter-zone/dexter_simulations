# Dexter Simulations

This repo contains helper scripts for testing the Dexter protocol on Persistence Network. Scripts are still a work in progress and are executed in an ad-hoc manner.

1. Create virtual environment

```
pip install virtualenv
python3 -m venv env
```

2. Install packages.

```
pip install cosmos_SDK
```

To work with persistence devnet, you need to add the following chain id config within the cosmos_SDK package,

    - Navigate to /env/lib../cosmos_sdk/client/lcd/lcdclient.py and add the following config to the `get_default` function

        ```
        if chain_id == "persistencecore":    # PERSISTENCE DEVNET
            return [Coins.from_str("0.15uxprt"), Numeric.parse(1.75)]
        ```

3. Execute testing scripts (ad-hoc)

   ```
   cd testnet_simulation
   ```

   ```
   python3 main.py
   ```
