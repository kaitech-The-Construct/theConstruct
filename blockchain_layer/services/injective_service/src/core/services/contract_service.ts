import {
  ChainGrpcWasmApi,
  ContractInfo,
  PaginationOption,
} from "@injectivelabs/sdk-ts";
import { getNetworkEndpoints, Network } from "@injectivelabs/networks";
import { NETWORK } from "./dex/services";

const endpoints = getNetworkEndpoints(NETWORK);
const chainGrpcWasmApi = new ChainGrpcWasmApi(endpoints.grpc);

async function fetchContractInfo(contractAddress) {
  const response = await chainGrpcWasmApi.fetchContractInfo(contractAddress);

  const contractInfo = response as ContractInfo;
  console.log(contractInfo);
  return contractInfo.codeId;
}

async function fetchContractAccountsBalance(contractAddress) {
  const pagination = {
    pageSize: 10,
    pageToken: "",
  } as PaginationOption;
  const contractAccountsBalance =
    await chainGrpcWasmApi.fetchContractAccountsBalance({
      contractAddress,
      pagination,
    });

  console.log(contractAccountsBalance);
}

async function fetchContractHistory(contractAddress) {
  const response = await chainGrpcWasmApi.fetchContractHistory(contractAddress);
  // const contractHistory = response as ContractHistoryResponse;
  console.log(response);
  return response;
}


