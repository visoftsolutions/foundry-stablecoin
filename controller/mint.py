import argparse
from decimal import Decimal
from subprocess import run

# Set up argparse
parser = argparse.ArgumentParser(description="Send a transaction using cast.")
parser.add_argument(
    "--rpc-url", default="https://polygon-rpc.com/", help="RPC URL to connect to"
)
parser.add_argument(
    "--gas-price", default="110gwei", help="Gas price for the transaction"
)
parser.add_argument("contract_address", help="Contract address to interact with")
parser.add_argument("--function_name", help="Function to call on the contract")
parser.add_argument("recipient_address", help="Recipient address for minting")
parser.add_argument(
    "mint_amount_ethers", type=Decimal, help="Amount to mint (in ethers)"
)

args = parser.parse_args()

# Convert the provided mint amount from ethers to wei
mint_amount_wei = int(args.mint_amount_ethers * 10**18)

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
        args.recipient_address,
        str(mint_amount_wei),
    ],
    capture_output=True,
)

output = completed.stdout.decode()
print(output)
