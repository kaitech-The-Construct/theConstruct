// token_creation.ts
import { clusterApiUrl, Connection, Keypair, PublicKey } from "@solana/web3.js";
import {
  createMint,
  getOrCreateAssociatedTokenAccount,
  mintTo,
  Account,
} from "@solana/spl-token";

import {
  Metadata,
  CreateMetadataArgs,
  
  Data,
  Creator
} from "@metaplex-foundation/mpl-token-metadata";

// Settings or constants, replace with actual values or import from a settings file
const NETWORK = clusterApiUrl("devnet"); // Using devnet for demo purpose

const DECIMALS = 0; // NFTs should have 0 decimals
const INITIAL_SUPPLY = 1; // Supply of 1 for uniqueness

/**
 * This should be a secure way of handling private keys. As of now, it's unsafe to store them in the code.
 * MASTER_PRIVATE_KEY should be a Uint8Array with 64 elements. You can generate it with Keypair.generate().secretKey.
 */
const MASTER_PRIVATE_KEY = new Uint8Array([/* Array of 64 numbers */]);
const MASTER_PUBLIC_KEY = new PublicKey("YourPublicKeyHere"); // Replace with actual public key

/**
 * Create a new SPL Token and associated NFT metadata.
 */
const keypair = Keypair.fromSecretKey(MASTER_PRIVATE_KEY);

// Helper to create metadata argument
function createMetadataData(name: string, symbol: string, uri: string): Data {
  return {
    name: name,
    symbol: symbol,
    uri: uri,
    sellerFeeBasisPoints: 500, // 5% fee
    creators: Option<Creator[]>,// Replace with an array of creators or null if not needed
  };
}

async function createNFT(): Promise<void> {
  try {
    // Establish connection to the Solana cluster
    const connection = new Connection(NETWORK, "confirmed");

    // Create a new token mint with supply of 1 to make it an NFT
    const mint = await createMint(
      connection,
      keypair, // Fee payer
      keypair.publicKey, // Mint Authority
      null, // Freeze Authority (null because NFTs shouldn't be freezable)
      DECIMALS
    );

    // Create an associated token account for the mint
    const tokenAccount = await getOrCreateAssociatedTokenAccount(
      connection,
      keypair,
      mint,
      keypair.publicKey
    );

    // Mint the NFT into the associated account
    await mintTo(
      connection,
      keypair,
      mint,
      tokenAccount.address,
      keypair.publicKey,
      INITIAL_SUPPLY
    );

    // Create the metadata for the NFT
    const metadataData = createMetadataData("Your NFT Name", "NFTSYMBOL", "https://your-metadata-url.com/metadata.json");

    let tx = await Metadata.create(
      connection,
      keypair,
      mint,
      keypair.publicKey,
      keypair.publicKey,
      new CreateMetadataArgs({ data: metadataData, isMutable: false })
    );

    // Log the mint, metadata, and transaction info
    console.log(`NFT Minted: ${mint.toBase58()}`);
    console.log(`Metadata: ${metadataData}`);
    console.log(`Transaction Signature: ${tx}`);
  } catch (error) {
    console.error("Error creating NFT:", error);
  }
}

// Execute the function to create the NFT
createNFT().then(() => console.log('NFT creation function executed.'));