import { getNetworkEndpoints, Network } from "@injectivelabs/networks";
import { SecretManagerServiceClient } from "@google-cloud/secret-manager";
import { ChainGrpcBankApi, IndexerGrpcSpotApi, IndexerGrpcDerivativesApi, IndexerGrpcDerivativesStream } from "@injectivelabs/sdk-ts";

// Function to access secret from GCP Secrets Manager
 export async function getSecret(name: string): Promise<string> {
  const project_id = process.env.PROJECTID || "";
  const secret_name = `projects/${project_id}/secrets/${name}/versions/latest`;

  const client = new SecretManagerServiceClient();
  try {
    const [version] = await client.accessSecretVersion({
      name: secret_name,
    });

    // Decode payload and convert to a string
    const secretData = version.payload?.data?.toString();

    if (secretData) {
      return secretData;
    } else {
      return '';
    }
  } catch (err) {
    console.error(`Error getting secret: ${err}`);
    throw new Error(`Error getting secret: ${err}`);
  }
}

// Contract Addresses
export const CW721_BASE_CONTRACT_ADDRESS = '';
export const OWNER_ADDRESS = ''



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

