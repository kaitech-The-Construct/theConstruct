import * as Koa from "koa";
import * as Router from "koa-router";

import {
  fetchAllNftInfo,
  fetchAllOperators,
  fetchAllTokens,
  fetchApproval,
  fetchApprovals,
  fetchContractInfo,
  fetchMinter,
  fetchNftInfo,
  fetchNumTokens,
  fetchOperator,
  fetchTokens,
} from "../core/services/cw721-base_query";

const nftQueryRouter = new Router({
  prefix: "/nft/queries",
});

// Function to handle Approval query
export async function approval(ctx: Koa.Context) {
  const token_id = ctx.params.token_id;
  const spender = ctx.params.spender;
  const include_expired = ctx.params.include_expired;
  const response = await fetchApproval(token_id, spender, include_expired);
  ctx.body = { message: "Approval query result", response: response };
}

// Function to handle Approvals query
export async function approvals(ctx: Koa.Context) {
  const token_id = ctx.params.token_id;
  const include_expired = ctx.params.include_expired;
  const response = await fetchApprovals(token_id, include_expired);
  ctx.body = { message: "Approvals query result", response: response };
}

// Function to handle Operator query
export async function operator(ctx: Koa.Context) {
  const owner = ctx.params.owner;
  const operator = ctx.params.operator;
  const include_expired = ctx.params.include_expired;
  const response = await fetchOperator(owner, operator, include_expired);
  ctx.body = { message: "Operator query result" };
}

// Function to handle AllOperators query
export async function allOperators(ctx: Koa.Context) {
  const owner = ctx.params.owner;
  const include_expired = ctx.params.include_expired;
  const start_after = ctx.params.start_after;
  const limit = ctx.params.limit;
  const response = await fetchAllOperators(
    owner,
    include_expired,
    start_after,
    limit
  );
  ctx.body = { message: "AllOperators query result", response: response };
}

// Function to handle NumTokens query
export async function numTokens(ctx: Koa.Context) {
  const contractAddress = ctx.params.contractAddress;
  const response = await fetchNumTokens(contractAddress);
  ctx.body = { message: "NumTokens query result", response: response };
}

// Function to handle ContractInfo query
export async function contractInfo(ctx: Koa.Context) {
  const contractAddress = ctx.params.contractAddress;
  const response = await fetchContractInfo(contractAddress);
  ctx.body = { message: "ContractInfo query result", response: response };
}

// Function to handle NftInfo query
export async function nftInfo(ctx: Koa.Context) {
  const token_id = ctx.params.token_id;
  const contractAddress = ctx.params.contractAddress;
  const response = await fetchNftInfo(contractAddress, token_id);
  ctx.body = { message: "NftInfo query result", response: response };
}

// Function to handle AllNftInfo query
export async function allNftInfo(ctx: Koa.Context) {
  const contractAddress = ctx.params.contractAddress;
  const token_id = ctx.params.token_id;
  const include_expired = ctx.params.include_expired;
  const response = await fetchAllNftInfo(
    contractAddress,
    token_id,
    include_expired
  );

  ctx.body = { message: "AllNftInfo query result", response: response };
}

// Function to handle Tokens query
export async function tokens(ctx: Koa.Context) {
  const contractAddress = ctx.params.contractAddress;
  const owner = ctx.params.owner;
  const start_after = ctx.params.start_after;
  const limit = ctx.params.limit;
  const response = await fetchTokens(
    contractAddress,
    owner,
    start_after,
    limit
  );
  ctx.body = { message: "Tokens query result", response: response };
}

// Function to handle AllTokens query
export async function allTokens(ctx: Koa.Context) {
  const contractAddress = ctx.params.contractAddress;
  const start_after = ctx.params.start_after;
  const limit = ctx.params.limit;
  const response = await fetchAllTokens(contractAddress, start_after, limit);
  ctx.body = { message: "AllTokens query result", response: response };
}

// Function to handle Minter query
export async function minter(ctx: Koa.Context) {
  const contractAddress = ctx.query.contractAddress.toString();
  const response = await fetchMinter(contractAddress);
  ctx.body = { message: "Minter query result" };
}

// Function to handle Extension query
export async function extension(ctx: Koa.Context) {}

nftQueryRouter.get("/approval/:contractAddress", approval);
nftQueryRouter.get("/approvals/:contractAddress", approvals);
nftQueryRouter.get("/operator/:contractAddress", operator);
nftQueryRouter.get("/all_operators/:contractAddress", allOperators);
nftQueryRouter.get("/num_tokens/:contractAddress", numTokens);
nftQueryRouter.get("/contract_info/:contractAddress", contractInfo);
nftQueryRouter.get("/nft_info/:token_id/:contractAddress", nftInfo);
nftQueryRouter.get("/all_nft_info/:contractAddress", allNftInfo);
nftQueryRouter.get("/tokens/:contractAddress", tokens);
nftQueryRouter.get("/all_tokens/:contractAddress", allTokens);
nftQueryRouter.get("/minter/:contractAddress", minter);
nftQueryRouter.get("/extension/:contractAddress", extension);

export default nftQueryRouter;
