import argparse
from decimal import Decimal
from subprocess import run

# Set up argparse
parser = argparse.ArgumentParser(description="Query balance using cast.")
parser.add_argument(
    "--rpc-url", default="https://polygon-rpc.com/", help="RPC URL to connect to"
)
parser.add_argument("contract_address", help="Contract address to interact with")
parser.add_argument(
    "--function_name",
    default="balanceOf(address)",
    help="Function to call on the contract",
)
parser.add_argument("query_address", help="Address to query balance for")

args = parser.parse_args()

# Use the provided arguments in the code
completed = run(
    [
        "cast",
        "call",
        "--rpc-url",
        args.rpc_url,
        args.contract_address,
        args.function_name,
        args.query_address,
    ],
    capture_output=True,
)

output = completed.stdout.decode()
balance = Decimal(int(output, 16))
print(f"balanceOf: {balance / 10**18}")
