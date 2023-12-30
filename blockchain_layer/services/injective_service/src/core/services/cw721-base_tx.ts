/// Execute Transactions
import { CW721_BASE_CONTRACT_ADDRESS, OWNER_ADDRESS } from "../config/settings";
import { broadcastTxWithPk } from "./private_msgBroadcaster";
import { MsgExecuteContractCompat } from "@injectivelabs/sdk-ts";
/**
 * Mint a new NFT and assign ownership to the specified address.
 * @param {string} token_id - Unique ID of the new NFT.
 * @param {string} owner - The owner's address to receive the new NFT.
 * @param {string | null} token_uri - Universal resource identifier for this NFT (optional).
 * @param {any} extension - Any custom extension data used by this contract (optional).
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function mint(
  token_id: string,
  owner: string,
  token_uri: string | null,
  extension?: any
) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      mint: {
        token_id,
        owner,
        token_uri,
        extension,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

/**
 * Grant approval to a spender for transferring/sending a specific token.
 * @param {string} spender - The address of the spender who receives approval.
 * @param {string} token_id - The ID of the token for which approval is granted.
 * @param {Expiration} expires - Optional expiration time for the approval.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function approve(spender: string, token_id: string, expires?: Boolean) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      approve: {
        spender,
        token_id,
        expires,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

/**
 * Revoke approval previously granted to a spender for a specific token.
 * @param {string} spender - The address of the spender whose approval is revoked.
 * @param {string} token_id - The ID of the token for which approval is revoked.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function revoke(spender: string, token_id: string) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      revoke: {
        spender,
        token_id,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

/**
 * Grant approval to an operator for transferring/sending any token owned by the owner.
 * @param {string} operator - The address of the operator who receives approval.
 * @param {Expiration} expires - Optional expiration time for the approval.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function approve_all(operator: string, expires?: Boolean) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      approve_all: {
        operator,
        expires,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

/**
 * Revoke operator approval previously granted to an operator.
 * @param {string} operator - The address of the operator whose approval is revoked.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function revoke_all(operator: string) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      revoke_all: {
        operator,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

/**
 * Send an NFT to a contract and trigger an action on the receiving contract.
 * @param {string} contract - The address of the contract to receive the NFT.
 * @param {string} token_id - The ID of the NFT to be sent.
 * @param {Binary} msg - The binary message to include with the NFT transfer.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function send_nft(contract: string, token_id: string, msg: any) {
  const message = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      send_nft: {
        contract,
        token_id,
        msg,
      },
    },
  });
  const response = await broadcastTxWithPk(message);
  console.log(response);
  return response;
}

/**
 * Burn (destroy) an NFT owned by the contract owner.
 * @param {string} token_id - The ID of the NFT to be burned.
 * @returns {Promise<any>} - A promise that resolves to the response of the transaction.
 */
async function burn(token_id: string) {
  const msg = MsgExecuteContractCompat.fromJSON({
    contractAddress: CW721_BASE_CONTRACT_ADDRESS,
    sender: OWNER_ADDRESS,
    msg: {
      burn: {
        token_id,
      },
    },
  });
  const response = await broadcastTxWithPk(msg);
  console.log(response);
  return response;
}

export { mint, approve, approve_all, revoke, revoke_all, burn, send_nft };
