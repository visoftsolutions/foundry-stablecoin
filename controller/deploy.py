import argparse
from subprocess import run

# Set up argparse
parser = argparse.ArgumentParser(description="Create a contract using forge.")
parser.add_argument(
    "--rpc-url", default="https://polygon-rpc.com/", help="RPC URL to connect to"
)
parser.add_argument(
    "--gas-price", default="110gwei", help="Gas price for the transaction"
)
parser.add_argument(
    "--constructor-args",
    nargs="*",
    default=[],
    help="Constructor arguments for the contract",
)
parser.add_argument(
    "contract_source_and_name", help="Contract source path and contract name"
)

args = parser.parse_args()

# Build the command list
cmd = [
    "forge",
    "create",
    "--rpc-url",
    args.rpc_url,
    "--trezor",
    "--gas-price",
    args.gas_price,
    *(["--constructor-args", *args.constructor_args] if args.constructor_args else []),
    args.contract_source_and_name,
]

# Run the command
completed = run(cmd, capture_output=True)

output = completed.stdout.decode()
print(output)
