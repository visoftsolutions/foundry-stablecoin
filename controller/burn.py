import argparse
from decimal import Decimal
from subprocess import run

# Set up argparse
parser = argparse.ArgumentParser(description="Burn tokens using cast.")
parser.add_argument(
    "--rpc-url", default="https://polygon-rpc.com/", help="RPC URL to connect to"
)
parser.add_argument(
    "--gas-price", default="110gwei", help="Gas price for the transaction"
)
parser.add_argument("contract_address", help="Contract address to interact with")
parser.add_argument(
    "--function_name", default="burn(uint256)", help="Function to call on the contract"
)
parser.add_argument(
    "burn_amount_ethers", type=Decimal, help="Amount to burn (in ethers)"
)

args = parser.parse_args()

# Convert the provided burn amount from ethers to wei
burn_amount_wei = int(args.burn_amount_ethers * 10**18)

# Use the provided arguments in the code
completed = run(
    [
        "cast",
        "send",
        "--rpc-url",
        args.rpc_url,
        "--trezor",
        "--gas-price",
        args.gas_price,
        args.contract_address,
        args.function_name,
        str(burn_amount_wei),
    ],
    capture_output=True,
)

output = completed.stdout.decode()
print(output)
