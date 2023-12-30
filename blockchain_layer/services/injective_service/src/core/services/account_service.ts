import { IndexerGrpcAccountPortfolioApi } from "@injectivelabs/sdk-ts";
import {
  WalletException,
  UnspecifiedErrorCode,
  ErrorType,
} from "@injectivelabs/exceptions";
import { getNetworkEndpoints } from "@injectivelabs/networks";
import { Wallet, WalletStrategy } from "@injectivelabs/wallet-ts";
import { ChainId } from "@injectivelabs/ts-types";
import { NETWORK } from "../config/settings";
import { Window as KeplrWindow } from "@keplr-wallet/types";

declare global {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface Window extends KeplrWindow {}
}

const endpoints = getNetworkEndpoints(NETWORK);
console.log(endpoints);

const indexerGrpcAccountPortfolioApi = new IndexerGrpcAccountPortfolioApi(
  endpoints.indexer
);

const walletStrategy = new WalletStrategy({
  chainId: ChainId.Testnet,
  wallet: Wallet.Keplr,
});

export async function connectWallet() {
  try {
    window.keplr.enable(ChainId.Testnet);

    const addresses = await walletStrategy.getAddresses();

    if (addresses.length === 0 || !addresses.every((address) => !!address)) {
      throw new WalletException(
        new Error("There are no addresses linked in this wallet."),
        {
          code: UnspecifiedErrorCode,
          type: ErrorType.WalletError,
        }
      );
    }

    console.log("Address: " + addresses[0]);
    return addresses[0];
  } catch (error) {
    console.error(error);
    return null; // Return a meaningful value, like null, to indicate an error.
  }
}

export async function getAccountPortfolio(address: string) {
  const portfolio =""
  await indexerGrpcAccountPortfolioApi.fetchAccountPortfolio(
    address
  );

  console.log(portfolio);
  return portfolio;
}
