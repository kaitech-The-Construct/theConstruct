import * as Koa from "koa";
import * as Router from "koa-router";
import { createSPLToken, getProgramAccounts } from "../services/tokenService";
import { SolanaApiResponse } from "../schemas/schema";

const mintRouter = new Router();

// Function to handle get wallet address and connect.
async function mintSPLToken(ctx: Koa.Context) {
  const response = await createSPLToken();
  if (response !== null) {
    ctx.body = { success: true, address: response };
  } else {
    ctx.body = { success: false, response: response };
  }
}

// Function to handle get account portfolio.
async function getProgramAccountsCall(ctx: Koa.Context) {
  const response = await getProgramAccounts();
//   const formattedResponse = response as SolanaApiResponse;
//   formattedResponse.result.forEach((account, index) => {
//     console.log(`Account ${index}: ` + JSON.stringify(account.account));
//   });
  ctx.body = { message: "Account retrieved.", response: response };
}

// Defining routes for the account functions
mintRouter.post("/mint", mintSPLToken);
mintRouter.get("/tokens", getProgramAccountsCall);

export default mintRouter;
