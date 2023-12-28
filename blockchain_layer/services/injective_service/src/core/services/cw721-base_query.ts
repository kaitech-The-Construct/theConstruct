import { CosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { getNetworkEndpoints } from "@injectivelabs/networks";
import { NETWORK } from "./dex/services";

const endpoints = getNetworkEndpoints(NETWORK);
const client = CosmWasmClient.connect(endpoints.rpc);

/**
 * Define a common function for executing queries.
 *
 * @param {string} contractAddress - The contract address to query.
 * @param {Record<string, any>} queryMsg - The query message to send to the contract.
 * @returns {Promise<T>} - A promise that resolves to the response of the query.
 */
async function executeQuery<T>(
  contractAddress: string,
  queryMsg: Record<string, any>
): Promise<T> {
  const response = await (
    await client
  ).queryContractSmart(contractAddress, queryMsg);
  console.log(response);
  return response;
}

/**
 * Fetches the NFT info for a given token ID.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} tokenId - The token ID of the NFT.
 * @returns {Promise<any>} - A promise that resolves to the NFT info.
 */
async function fetchNftInfo(contractAddress: string, tokenId: string) {
  const queryMsg = { nft_info: { token_id: tokenId } };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Fetches all NFT info for a given token ID.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} tokenId - The token ID of the NFT.
 * @param {boolean} includeExpired - Whether to include expired NFTs in the response.
 * @returns {Promise<any>} - A promise that resolves to all NFT info.
 */
async function fetchAllNftInfo(
  contractAddress: string,
  tokenId: string,
  includeExpired?: boolean
) {
  const queryMsg = {
    all_nft_info: { token_id: tokenId, include_expired: includeExpired },
  };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Fetch an operator for a given owner and operator.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} owner - The owner's address.
 * @param {string} operator - The operator's address.
 * @param {boolean} includeExpired - Whether to include expired operators in the response.
 * @returns {Promise<any>} - A promise that resolves to the operator response.
 */
async function fetchOperator(
  contractAddress: string,
  owner: string,
  operator: string,
  includeExpired?: boolean
) {
  const queryMsg = {
    operator: {
      owner: owner,
      operator: operator,
      include_expired: includeExpired,
    },
  };
  return executeQuery(contractAddress, queryMsg);
}


/**
 * Lists all operators that can access all of the owner's tokens.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} owner - The owner's address.
 * @param {boolean} includeExpired - Whether to include expired operators in the response.
 * @param {string} startAfter - The starting token ID to list operators from.
 * @param {number} limit - The maximum number of operators to list.
 * @returns {Promise<any>} - A promise that resolves to a list of operators.
 */
async function fetchAllOperators(
  contractAddress: string,
  owner: string,
  includeExpired?: boolean,
  startAfter?: string,
  limit?: number
) {
  const queryMsg = {
    all_operators: {
      owner,
      include_expired: includeExpired,
      start_after: startAfter,
      limit,
    },
  };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Returns the total number of tokens issued.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @returns {Promise<any>} - A promise that resolves to the total number of tokens.
 */
async function fetchNumTokens(contractAddress: string) {
  const queryMsg = { num_tokens: {} };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * With MetaData Extension.
 * Returns top-level metadata about the contract.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @returns {Promise<any>} - A promise that resolves to the contract metadata.
 */
async function fetchContractInfo(contractAddress: string) {
  const queryMsg = { contract_info: {} };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * With Enumerable extension.
 * Returns all tokens owned by the given address.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} owner - The owner's address.
 * @param {string} startAfter - The starting token ID to list tokens from.
 * @param {number} limit - The maximum number of tokens to list.
 * @returns {Promise<any>} - A promise that resolves to a list of tokens.
 */
async function fetchTokens(
  contractAddress: string,
  owner: string,
  startAfter?: string,
  limit?: number
) {
  const queryMsg = { tokens: { owner, start_after: startAfter, limit } };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * With Enumerable extension.
 * Lists all token_ids controlled by the contract.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} startAfter - The starting token ID to list tokens from.
 * @param {number} limit - The maximum number of tokens to list.
 * @returns {Promise<any>} - A promise that resolves to a list of tokens.
 */
async function fetchAllTokens(
  contractAddress: string,
  startAfter?: string,
  limit?: number
) {
  const queryMsg = { all_tokens: { start_after: startAfter, limit } };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Return the minter.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @returns {Promise<any>} - A promise that resolves to the minter.
 */
async function fetchMinter(contractAddress: string) {
  const queryMsg = { minter: {} };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Extension query.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {Q} msg - The extension query message.
 * @returns {Promise<any>} - A promise that resolves to the extension query response.
 */
async function fetchExtension<Q>(contractAddress: string, msg: Q) {
  const queryMsg = { extension: { msg } };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Approve a spender to spend a token.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} tokenId - The token ID to approve.
 * @param {string} spender - The address of the spender to approve.
 * @param {boolean} include_expired - Whether the approval should expire.
 * @returns {Promise<any>} - A promise that resolves to the approval response.
 */
async function fetchApproval(
  contractAddress: string,
  tokenId: string,
  spender: string,
  include_expired?: boolean
) {
  const queryMsg = {
    approve: {
      token_id: tokenId,
      spender: spender,
      include_expired: include_expired,
    },
  };
  return executeQuery(contractAddress, queryMsg);
}

/**
 * Approve all tokens for a spender.
 *
 * @param {string} contractAddress - The contract address of the NFT contract.
 * @param {string} operator - The address of the operator to approve.
 * @param {boolean} include_expired - Whether the approval should expire.
 * @returns {Promise<any>} - A promise that resolves to the approve all response.
 */
async function fetchApprovals(
  contractAddress: string,
  operator: string,
  include_expired?: boolean
) {
  const queryMsg = {
    approve_all: {
      operator: operator,
      include_expired: include_expired,
    },
  };
  return executeQuery(contractAddress, queryMsg);
}

export {
  fetchOperator,
  fetchAllOperators,
  fetchNumTokens,
  fetchContractInfo,
  fetchNftInfo,
  fetchAllNftInfo,
  fetchTokens,
  fetchAllTokens,
  fetchMinter,
  fetchExtension,
  fetchApproval,
  fetchApprovals,
};
