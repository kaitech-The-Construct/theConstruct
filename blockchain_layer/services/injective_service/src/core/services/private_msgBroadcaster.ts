import {
  MsgMint,
  MsgBroadcasterWithPk,
  MsgCreateDenom,
  MsgSetDenomMetadata,
} from "@injectivelabs/sdk-ts";
import { BigNumberInBase } from "@injectivelabs/utils";
import { Network } from "@injectivelabs/networks";
import {
  MsgBroadcaster,
  Wallet,
  WalletStrategy,
} from "@injectivelabs/wallet-ts";
import { ChainId } from "@injectivelabs/ts-types";
import { MsgSend } from "@injectivelabs/sdk-ts";
import { NETWORK } from "./dex/services";
import { getSecret } from "../config/settings";

const walletStrategy = new WalletStrategy({
  chainId: ChainId.Testnet,
  wallet: Wallet.Keplr,
});

const msgBroadcastClient = new MsgBroadcaster({
  walletStrategy /* instantiated wallet strategy */,
  network: NETWORK,
});

// Utility function for transaction broadcasting
export async function broadcastTxWithPk(msg: any): Promise<string> {
  // PRIVATE KEY
  const privateKey = await getSecret("injective_master_private");
  // Pre-configured MsgBroadcasterWithPk instance
  const msgBroadcasterWithPk = new MsgBroadcasterWithPk({
    privateKey,
    network: NETWORK,
  });
  const txHash = await msgBroadcasterWithPk.broadcast({
    msgs: [msg],
  });
  console.log(txHash);
  return txHash.txHash;
}
export async function broadcastTxWithWalletStrategy(msg: any): Promise<string> {
  const txHash = await msgBroadcastClient.broadcast({
    msgs: [msg],
  });
  console.log(txHash);
  return txHash.txHash;
}
