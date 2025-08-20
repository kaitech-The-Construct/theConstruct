import * as views from '@ladjs/koa-views';
import * as Koa from 'koa';
import * as bodyParser from 'koa-bodyparser';
import * as json from 'koa-json';
import * as Router from 'koa-router';
import * as serve from 'koa-static';

import * as path from 'path';
import mintRouter from './api/api';

const app = new Koa();

const router = new Router();

// Middleware to handle json responses
app.use(json());
// Middleware to parse request bodies
app.use(bodyParser());

// Routers
// app.use(adminRouter.routes()).use(adminRouter.allowedMethods());

app.use(router.routes());
app.use(mintRouter.routes());
app.use(views(path.join(__dirname, 'templates'), {extension: 'ejs'})); 
app.use(serve(path.join(__dirname, 'static')));
// Define a route to render an HTML page
app.use(async ctx => {

  await ctx.render('index', {title: 'SPL Manager'});
});
// Start the server
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});

export default app;
