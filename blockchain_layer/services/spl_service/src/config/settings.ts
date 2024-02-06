import { SecretManagerServiceClient } from "@google-cloud/secret-manager";

// Function to access secret from GCP Secrets Manager
async function getSecret(name: string): Promise<string> {
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

// settings.ts

// Define the network endpoint to connect to
export const NETWORK_LOCAL = "http://127.0.0.1:8899";
export const SOLANA_RPC_ENDPOINT_MAINNET = "https://api.mainnet-beta.solana.com"
export const SOLANA_RPC_ENDPOINT_DEVNET = "https://api.devnet.solana.com"
export const SOLANA_RPC_ENDPOINT_TESTNET = "https://api.testnet.solana.com"
export const MAINNET = "mainnet"
export const DEVNET = "devnet"
export const TESTNET = "testnet"

// Test account addresses
export const TEST_ACCOUNT_1 = "DFn5xHxmWHu12rbCn658668p7LUcVzhyemat3p3RkcQ9"
export const TEST_ACCOUNT_2 = "GWbH5iQqdC3FMTKHu1bDYNocknp42ZPNg6GU9wgLJFgt"


export const MASTER_PUBLIC_KEY = "DaXypSCCzTiXkctgByCyLsWVzfauME3A3xM8Nos3PUhr"
export const MASTER_PRIVATE_KEY = Uint8Array.from([
  17, 215, 181, 184,  78, 116, 116, 191, 101, 130,  87,
  15,  27, 206, 224, 219, 147,  27, 182, 173,  20, 219,
  29,  16, 166,  52,  79, 213, 195,  18, 127,  42, 186,
 227, 112,  70, 220, 110, 125,  64, 230, 123,  57, 119,
  57,  89, 124, 122,  20, 203, 251, 214, 251, 189, 175,
  45, 224, 247,  88, 156, 222,  36,  37, 221
])

// Define the public key for the Solana Token Program
// The official Solana Token Program ID is used for interacting with the SPL token standard
export const TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA";

// Define the public key for the Solana Associated Token Account Program
// (this program finds or creates an associated token account for a wallet address & SPL token mint)
export const ASSOCIATED_TOKEN_PROGRAM_ID = "ATokenGPuVDgSg6o58BrY40zwf7GJnitxPWE7tu5gZfX";

// Define the public keys for any other programs you might interact with
export const OTHER_PROGRAM_ID = "YourOtherProgramPublicKeyHere";

// Define any additional configuration settings that are relevant for your service
// For example, a fee payer wallet address or the address of a specific token mint
export const FEE_PAYER_WALLET_ADDRESS = "YourFeePayerWalletPublicKeyHere";
export const TOKEN_MINT_ADDRESS = "YourTokenMintPublicKeyHere";

// If you want to configure commitment levels for RPC requests, you can specify them here
export const COMMITMENT = "confirmed";

// Default transaction confirmation timeout in milliseconds
export const TX_CONFIRMATION_TIMEOUT = 30000; // 30 seconds

// You can also include other settings that might be needed for your application
export const MAX_TRANSACTION_SIZE = 1232; // in bytes