// Define models for the Solana API response
export interface TokenAccountInfo {
    isNative: boolean;
    mint: string;
    owner: string;
    state: string;
    tokenAmount: {
      amount: string;
      decimals: number;
      uiAmount: number;
      uiAmountString: string;
    };
  }
  
  export interface Account {
    data: {
      parsed: {
        info: TokenAccountInfo;
        type: string;
      };
      program: string;
      space: number;
    };
    executable: boolean;
    lamports: number;
    owner: string;
    rentEpoch: number;
    space: number;
  }
  
  export interface SolanaApiResponse {
    jsonrpc: string;
    result: {
      account: Account;
      pubkey: string;
    }[];
    id: number;
  }
  