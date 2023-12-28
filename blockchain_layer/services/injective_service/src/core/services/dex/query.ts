// filename: Query.ts
import  { getDefaultSubaccountId, OrderbookWithSequence } from '@injectivelabs/sdk-ts'
import {
  chainBankApi,
  indexerSpotApi,
  indexerSpotStream,
  indexerDerivativesApi,
  indexerDerivativeStream,
} from './services'

export const fetchDerivativeMarkets = async () => {
  return await indexerDerivativesApi.fetchMarkets()
}

export const fetchPositions = async (injectiveAddress: string) => {
  const subaccountId = getDefaultSubaccountId(injectiveAddress)

  return await indexerDerivativesApi.fetchPositions({ subaccountId })
}

export const fetchSpotMarkets = async () => {
  return await indexerSpotApi.fetchMarkets()
}

export const fetchBankBalances = async (injectiveAddress: string) => {
  return await chainBankApi.fetchBalances(injectiveAddress)
}

export const streamDerivativeMarketOrderbook = async (
  marketId: string,
  ) => {
  const streamOrderbookUpdates = indexerDerivativeStream.streamDerivativeOrderbookUpdate.bind(indexerDerivativeStream)
  const callback = (orderbookUpdate) => {
    console.log(orderbookUpdate)
  }

  streamOrderbookUpdates({
    marketId,
    callback
  })
}

export const streamSpotMarketOrderbook = async (
  marketId: string,
  ) => {
  const streamOrderbookUpdates = indexerSpotStream.streamDerivativeOrderbookUpdate.bind(indexerSpotStream)
  const callback = (orderbookUpdate) => {
    console.log(orderbookUpdate)
  }

  streamOrderbookUpdates({
    marketId,
    callback
  })
}