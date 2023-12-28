export interface MintMsg {
    token_id: string;
    owner: string;
    token_uri?: string | null;
    extension?: any;
  }
  
  export interface ApproveMsg {
    spender: string;
    token_id: string;
    expires?: Boolean;
  }
  
  export interface RevokeMsg {
    spender: string;
    token_id: string;
  }
  
  export interface ApproveAllMsg {
    operator: string;
    expires?: Boolean;
  }
  
  export interface RevokeAllMsg {
    operator: string;
  }
  
  export interface SendNftMsg {
    contract: string;
    token_id: string;
    msg: any;
  }
  
  export interface BurnMsg {
    token_id: string;
  }
  