import argparse
from decimal import Decimal
from subprocess import run

# Set up argparse
parser = argparse.ArgumentParser(description="Get information from a token contract.")
parser.add_argument("token_address", help="Token contract address")
parser.add_argument(
    "--rpc-url", default="https://polygon-rpc.com/", help="RPC URL to connect to"
)
parser.add_argument(
    "--function", default="totalSupply()", help="Function to call on the token contract"
)

args = parser.parse_args()

# Use the provided arguments in the code
completed = run(
    [
        "cast",
        "call",
        "--rpc-url",
        args.rpc_url,
        args.token_address,
        args.function,
    ],
    capture_output=True,
)
output = completed.stdout.decode()
total_supply = Decimal(int(output, 16))
print(f"totalSupply in wei: {total_supply}")
print(f"totalSupply in ethers: {total_supply / 10**18}")
