import { clusterApiUrl, Connection, Keypair, LAMPORTS_PER_SOL } from '@solana/web3.js';


async function requestAndConfirmAirdrop(): Promise<void> {
  const payer = Keypair.generate();
  const connection = new Connection(clusterApiUrl('testnet'), 'confirmed');
  const airdropSignature = await connection.requestAirdrop(
    payer.publicKey,
    LAMPORTS_PER_SOL
  );
  await connection.confirmTransaction(airdropSignature);
}


