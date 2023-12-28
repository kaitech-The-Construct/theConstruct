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
  export const NETWORK = Network.TestnetSentry;
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

// Contract Addresses
export const CW721_BASE_CONTRACT_ADDRESS = 'inj1hm7hfga0tuq078dq7fr3xwkt8gzzj36q99m2q3';
export const OWNER_ADDRESS = 'inj1v29felst8txy2exz8k8z3udjuww86s9xnn7dka'