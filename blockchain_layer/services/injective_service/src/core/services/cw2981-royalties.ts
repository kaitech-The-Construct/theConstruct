import { CosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { getNetworkEndpoints } from "@injectivelabs/networks";
import { NETWORK } from "../config/settings";
import { BigNumberInBase } from '@injectivelabs/utils';


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
 * Fetch Royalty Info
 *
 * @param {string} contractAddress - The contract address to query.
 * @param {token_id} token_id - The token id to query.
 * @param {sale_price} sale_price - The sale price to query.
 * @returns {Promise<T>} - A promise that resolves to the response of the query.
 */
export async function fetchRoyaltyInfoByTokenId(
  contractAddress: string,
  token_id: string,
  sale_price: BigNumberInBase
) {
  return executeQuery(contractAddress, {
    royaltyInfo: {
      token_id: token_id,
      sale_price: sale_price
    },
  });
}

/**
 * Check Royalties *
 * @param {string} contractAddress - The contract address to query.
 * @returns {Promise<T>} - A promise that resolves to the response of the query.
 */
export async function checkRoyalties(
  contractAddress: string,
) {
  return executeQuery(contractAddress, {
    checkRoyalties: {},
  });
}

 
