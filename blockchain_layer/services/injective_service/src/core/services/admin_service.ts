// import {
//   MsgMint,
//   MsgBroadcasterWithPk,
//   MsgCreateDenom,
//   MsgSetDenomMetadata,
// } from "@injectivelabs/sdk-ts";
// import { BigNumberInBase } from "@injectivelabs/utils";
// import { Network } from "@injectivelabs/networks";
// import {
//   MsgBroadcaster,
//   Wallet,
//   WalletStrategy,
// } from "@injectivelabs/wallet-ts";
// import { ChainId } from "@injectivelabs/ts-types";
// import { MsgSend } from "@injectivelabs/sdk-ts";

// // Configuration

// const NETWORK = Network.TestnetK8s;
// const amountInBase = new BigNumberInBase(10000);

// const amountToBurn = amountInBase.toWei(6).toFixed();
// const logo = encodeURI(
//   "https://storage.googleapis.com/app-images-the-construct-401518/logo.png"
// );

// // Pre-configured MsgBroadcasterWithPk instance
// const msgBroadcasterWithPk = new MsgBroadcasterWithPk({
//   privateKey,
//   network: NETWORK,
// });

// const walletStrategy = new WalletStrategy({
//   chainId: ChainId.Testnet,
//   wallet: Wallet.Keplr,
// });

// const msgBroadcastClient = new MsgBroadcaster({
//   walletStrategy /* instantiated wallet strategy */,
//   network: NETWORK,
// });
// // Utility function for transaction broadcasting
// async function broadcastTx(msg: any): Promise<string> {
//   const txHash = await msgBroadcasterWithPk.broadcast({
//     msgs: [msg],
//   });
//   console.log(txHash);
//   return txHash.txHash;
// }

// // Token management functions
// export async function createToken(subdenom:string) {
//   const msg = MsgCreateDenom.fromJSON({
//     subdenom,
//     sender: injectiveAddress,
//   });
//   return await broadcastTx(msg);
// }

// export async function mintToken(amount: string) {
//   const amountInBase = new BigNumberInBase(amount);
//   const amountToMint = amountInBase.toWei(6).toFixed();

//   const msg = MsgMint.fromJSON({
//     sender: injectiveAddress,
//     amount: {
//       denom: `factory/${injectiveAddress}/${subdenom}`,
//       amount: amountToMint,
//     },
//   });

//   return await broadcastTx(msg);
// }

// export async function sendToken(destination: string) {
//   const msg = MsgSend.fromJSON({
//     amount: {
//       denom: `factory/${injectiveAddress}/${subdenom}`,
//       amount: amountToBurn,
//     },
//     srcInjectiveAddress: injectiveAddress,
//     dstInjectiveAddress: destination,
//   });

//   return await broadcastTx(msg);
// }

// const denomUnitsIfTokenHas6Decimals = [
//   {
//     denom: denom /** we use the whole denom here */,
//     exponent: 0,
//     aliases: [`micro${subdenom}`],
//   },
//   {
//     denom: subdenom,
//     exponent: 6 /** we use the subdenom only here (if you want your token to have 6 decimals) */,
//     aliases: [subdenom],
//   },
// ];

// export async function setMetadata() {
//   const msg = MsgSetDenomMetadata.fromJSON({
//     sender: injectiveAddress,
//     metadata: {
//       base: denom /** the base denom */,
//       description:
//         "Test Tokens for The Construct DEX" /** description of your token */,
//       display:
//         subdenom /** the display alias of your token on UIs (it's the denom of the unit with highest decimals) */,
//       name: "robo-test" /** the name of your token */,
//       symbol: "RBT" /** the symbol of your token */,
//       uri: logo /** the logo of your token, should be hosted on IPFS and should be a small webp image */,
//       uriHash: null,
//       denomUnits:
//         denomUnitsIfTokenHas6Decimals /** choose if you want to have 6 or 0 decimals for the token */,
//     },
//   });

//   return await broadcastTx(msg);
// }
