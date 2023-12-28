interface BankBalance {
    amount: string;
    denom: string;
  }
  
  interface AccountInfo {
    accountAddress: string;
    bankBalancesList: BankBalance[];
    subaccountsList: any[]; // You can specify the types for subaccountsList and positionsWithUpnlList if needed
    positionsWithUpnlList: any[]; // You can specify the types for subaccountsList and positionsWithUpnlList if needed
  }
  
  // NFT Execution and Query Messages
export interface TransferNftMsg {
  recipient: string;
  token_id: string;
}

export interface TransferNftResponse {
  message: string;
}

export interface QueryNftMsg {
  token_id: string;
}

export interface QueryNftResponse {
  message: string;
}


// Contract Responses
export interface ContractInfoResponse{
  "codeId": number,
  "creator": string,
  "admin": string,
  "label": string,
  "created": {
    "blockHeight": number,
    "txIndex": number
  },
  "ibcPortId": string
}


export interface ContractHistoryResponse {
  entriesList: [
    {
      operation: number;
      codeId: number;
      updated: [Object];
      msg: [Uint8Array];
    }
  ];
  pagination: { total: number; next: string };
}
