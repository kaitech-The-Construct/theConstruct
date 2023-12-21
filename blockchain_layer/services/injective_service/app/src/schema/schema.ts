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
  