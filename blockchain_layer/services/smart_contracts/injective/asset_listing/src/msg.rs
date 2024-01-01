use cosmwasm_std::{ Addr, Coin};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, JsonSchema)]
pub struct InstantiateMsg {
    pub owner: Addr,
}

#[derive(Serialize, Deserialize, JsonSchema)]
pub enum ExecuteMsg {
    CreateListing {
        listing_id: u64,
        token_id: String,
        prices: Vec<Coin>,
        quantity: u64,
    },
    CancelListing {
        listing_id: u64,
    },
    
}

#[derive(Serialize, Deserialize, JsonSchema)]
pub enum QueryMsg {
    GetListing {
        listing_id: u64,
    },
    GetState,
}