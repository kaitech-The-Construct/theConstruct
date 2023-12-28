import * as Koa from "koa";
import * as bodyParser from "koa-bodyparser";
import * as json from "koa-json";
import * as Router from "koa-router";
import * as views from "@ladjs/koa-views";
import * as serve from "koa-static";
import accountRouter from "./routers/account";
import path = require("path");
import nftQueryRouter from "./routers/nft_queries";

const app = new Koa();

const router = new Router();

// Middleware to handle json responses
app.use(json());
// Middleware to parse request bodies
app.use(bodyParser());

// Routers
// app.use(adminRouter.routes()).use(adminRouter.allowedMethods());
app.use(accountRouter.routes()).use(accountRouter.allowedMethods());
app.use(nftQueryRouter.routes()).use(nftQueryRouter.allowedMethods())
app.use(router.routes());
app.use(views(path.join(__dirname, "../templates"), { extension: "ejs" })); // Replace 'ejs' with your template engine
app.use(serve(path.join(__dirname, "../static")));
// Define a route to render an HTML page
app.use(async (ctx) => {
  // Replace 'template' with the name of your HTML template file (without the extension)
  await ctx.render("index", { title: "DREX" });
});
// Start the server
app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});

export default app;
