// import * as Koa from 'koa';
// import * as Router from 'koa-router';
// import { mintToken, sendToken } from '../core/services/admin_service';

// const adminRouter = new Router({ 
//     prefix: '/admin'
// });

// // Function to handle minting of tokens.
// async function mintTokenCall(ctx: Koa.Context) {
//     const amount = ctx.params.amount;
//     const response = await mintToken(amount); 
//     ctx.body = { message: 'Token minted successfully', response:response };
// }

// // Function to handle sending of tokens.
// async function sendTokenCall(ctx: Koa.Context) {
//     const destination = ctx.params.destination;
//     const response = await sendToken(destination);
//     ctx.body = { message: 'Token sent successfully', response:response };
// }

// // Function to handle setting metadata.
// async function setMetadataCall(ctx: Koa.Context) {
//     // Logic to set metadata...
//     ctx.body = { message: 'Metadata set successfully' };
// }

// // Function to handle creation of tokens.
// async function createTokenCall(ctx: Koa.Context) {
//     const tokenName = ctx.params.name;
//     const response = await sendToken(tokenName);
//     ctx.body = { message: 'Token created successfully', response:response  };
// }

// // Defining routes for the admin panel
// adminRouter.post('/mintToken/:amount', mintTokenCall);
// adminRouter.post('/sendToken/:destination', sendTokenCall);
// adminRouter.post('/setMetadata', setMetadataCall);
// adminRouter.post('/createToken/:name', createTokenCall);

// // Export the adminRouter

// export default adminRouter;
