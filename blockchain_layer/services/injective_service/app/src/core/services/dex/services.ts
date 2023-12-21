// filename: Services.ts
import {
    ChainGrpcBankApi,
    IndexerGrpcSpotApi,
    IndexerGrpcDerivativesApi,
    IndexerGrpcDerivativesStream,
  } from "@injectivelabs/sdk-ts";
  import { getNetworkEndpoints, Network } from "@injectivelabs/networks";
  
  // Getting the pre-defined endpoints for the Testnet environment
  // (using TestnetK8s here because we want to use the Kubernetes infra)
  export const NETWORK = Network.TestnetK8s;
  export const ENDPOINTS = getNetworkEndpoints(NETWORK);
  
  export const chainBankApi = new ChainGrpcBankApi(ENDPOINTS.grpc);
  export const indexerSpotApi = new IndexerGrpcSpotApi(ENDPOINTS.indexer);
  export const indexerDerivativesApi = new IndexerGrpcDerivativesApi(
    ENDPOINTS.indexer
  );
  
  export const indexerSpotStream = new IndexerGrpcDerivativesStream(
    ENDPOINTS.indexer
  );
  export const indexerDerivativeStream = new IndexerGrpcDerivativesStream(
    ENDPOINTS.indexer
  );