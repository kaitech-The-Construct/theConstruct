import * as Koa from "koa";
import * as bodyParser from "koa-bodyparser";
import * as json from "koa-json";
import * as views from "@ladjs/koa-views";
import * as serve from "koa-static";

import path = require("path");
import accountRouter from "./routers/account";
import nftQueryRouter from "./routers/nft_queries";

const app = new Koa();

// Middleware to handle json responses
app.use(json());
// Middleware to parse request bodies
app.use(bodyParser());

// Routers
// app.use(adminRouter.routes()).use(adminRouter.allowedMethods());
app.use(accountRouter.routes()).use(accountRouter.allowedMethods());
app.use(nftQueryRouter.routes()).use(nftQueryRouter.allowedMethods())

app.use(views(path.join(__dirname, "../templates"), { extension: "ejs" })); // Replace 'ejs' with your template engine
app.use(serve(path.join(__dirname, "../static")));
// Define a route to render an HTML page
app.use(async (ctx) => {
  // Replace 'template' with the name of your HTML template file (without the extension)
  await ctx.render("index", { title: "DREX" });
});

// Start the server
app.listen(8080, () => {
  console.log("Server running on http://localhost:8080");
});


export default app;
