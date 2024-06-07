import * as Koa from 'koa';
import * as Router from "koa-router";
import {
  connectWallet,
  getAccountPortfolio,
} from "../core/services/account_service";

const accountRouter = new Router({
  prefix: "/account",
});

// Function to handle get wallet address and connect.
async function getWalletAddress(ctx: Koa.Context) {
  const response = await connectWallet();
  if (response !== null) {
    console.log(response);
    ctx.body = { success: true, address: response };
  } else {
    ctx.body = { success: false, response: response };
  }
}

// Function to handle get account portfolio.
async function getPortfolioAccount(ctx: Koa.Context) {
  const address = ctx.params.address;
  const response = await getAccountPortfolio(address);
  ctx.body = { message: "Account retrieved.", response: response };
}

// Defining routes for the account functions
accountRouter.get("/connect", getWalletAddress);
accountRouter.get("/:address", getPortfolioAccount);

export default accountRouter;
