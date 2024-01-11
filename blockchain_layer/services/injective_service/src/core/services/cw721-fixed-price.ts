import { CosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { getNetworkEndpoints } from "@injectivelabs/networks";
import { NETWORK } from "../config/settings";


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
 * Fetches config parameters from the contract.
 *
 * @param {string} contractAddress - The contract address to query.
 * @returns {Promise<any>} - A promise that resolves to the contract config.
 */
export async function fetchConfig(contractAddress: string) {
  const queryMsg = { getConfig: {} };
  return executeQuery(contractAddress, queryMsg);
}