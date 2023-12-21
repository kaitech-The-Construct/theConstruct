import {
  IndexerGrpcAccountPortfolioApi,
  IndexerGrpcAccountApi,
  getEthereumAddress,
} from "@injectivelabs/sdk-ts";
import {
  WalletException,
  UnspecifiedErrorCode,
  ErrorType,
} from "@injectivelabs/exceptions";
import { getNetworkEndpoints, Network } from "@injectivelabs/networks";
import {
  MsgBroadcaster,
  Wallet,
  WalletStrategy,
} from "@injectivelabs/wallet-ts";
import { ChainId } from "@injectivelabs/ts-types";

const endpoints = getNetworkEndpoints(Network.TestnetK8s);
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
    const addresses = await walletStrategy.getAddresses();

    if (addresses.length === 0) {
      throw new WalletException(
        new Error("There are no addresses linked in this wallet."),
        {
          code: UnspecifiedErrorCode,
          type: ErrorType.WalletError,
        }
      );
    }

    if (!addresses.every((address) => !!address)) {
      throw new WalletException(
        new Error("There are no addresses linked in this wallet."),
        {
          code: UnspecifiedErrorCode,
          type: ErrorType.WalletError,
        }
      );
    }

    return addresses[0];
  } catch (error) {
    console.log(error);
    return;
  }
}

export async function getAccountPortfolio(address: string) {
  const portfolio = await indexerGrpcAccountPortfolioApi.fetchAccountPortfolio(
    address
  );

  console.log(portfolio);
  return portfolio;
}
