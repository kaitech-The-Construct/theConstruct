# Payment Handler

The Payment Handler is a blockchain-based smart contract developed for the CosmWasm platform. It handles escrow transactions, enabling secure and trustless payments between parties. This contract ensures that funds are only released when certain pre-agreed conditions have been met.

## Features

- **Escrow Creation**: Users can create escrow agreements by locking in funds meant for another party.
- **Time-based Release**: Funds within the escrow can be set to release after a predetermined time frame has elapsed.
- **Secure**: A simple yet secure mechanism for ensuring trustless transactions.

## Deployment

Before deploying the contract, make sure you have `rust` and `cargo` installed, along with the `cargo generate` tool for CosmWasm smart contracts.

If you are deploying to a testnet or mainnet, you will need to have the `wasmd` CLI tool installed, as well as a wallet with sufficient funds for contract upload and instance creation.

### Compile

To compile the contract, run:

```sh
cargo wasm

Contract address: inj19emwplyuwe0rcdp4gpau9e6jgch9mzjrhqyrer