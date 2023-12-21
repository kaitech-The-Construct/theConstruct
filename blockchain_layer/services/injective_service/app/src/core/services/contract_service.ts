import { CosmWasmClient, SigningCosmWasmClient } from '@cosmjs/cosmwasm-stargate';
import {
    MsgBroadcaster,
    Wallet,
    WalletStrategy,
  } from "@injectivelabs/wallet-ts";

async function deployAndQueryContract(contractCode: Uint8Array, initArgs: object, queryArgs: object): Promise<any> {
    // Set up the wallet and client
    // const wallet = await Wallet.fromMnemonic('<your-mnemonic>');
    const client = await CosmWasmClient.connect('<rpc-endpoint>');
    
    // Instantiate the contract
    const instantiateResponse = await client.instantiate(wallet, codeId, initArgs, "My Contract");
    const contractAddress = instantiateResponse.contractAddress;
    
    // Query the contract
    const queryResponse = await client.queryContractSmart(contractAddress, queryArgs);
    
    return queryResponse;
}

// Example usage
const contractCode = new Uint8Array([...]);  // This should be the compiled contract code
const initArgs = { count: 0 };
const queryArgs = { get_count: {} };
deployAndQueryContract(contractCode, initArgs, queryArgs).then(response => {
    console.log(response);
});