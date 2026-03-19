// InjectiveApi.ts
import { InjectiveClient, Account, Market, Trade } from '@injectivelabs/sdk-ts';
import { Web3Provider } from '@ethersproject/providers';
import { BigNumber } from 'ethers';

class InjectiveApi {
    private client: InjectiveClient;
    private account: Account;

    constructor(injectiveEndpoint: string, privateKey: string) {
        const web3Provider = new Web3Provider(window.ethereum);
        this.client = new InjectiveClient({ endpoint: injectiveEndpoint });
        this.account = new Account(privateKey, web3Provider);
    }

    async initialize() {
        await this.account.connect();
        this.client.start(this.account.getAddress());
    }

    async getMarkets(): Promise<Market[]> {
        return await this.client.getMarkets();
    }

    async getMarket(marketId: string): Promise<Market> {
        return await this.client.getMarket(marketId);
    }

    async getTrades(marketId: string): Promise<Trade[]> {
        return await this.client.getTrades(marketId);
    }

    async submitOrder(order): Promise<void> {
        const { marketId, amount, price, side } = order;
        const bigNumberPrice = new BigNumber(price);
        const bigNumberQuantity = new BigNumber(amount);
        await this.client.submitOrder({
            marketId,
            quantity: bigNumberQuantity,
            price: bigNumberPrice,
            side
        });
    }

    // Add more functions for each type of API call required by the bot, such as withdraw, deposit, getPositions, etc.
}

export default InjectiveApi;