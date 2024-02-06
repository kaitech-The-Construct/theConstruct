use cosmwasm_std::{Addr, Uint128, StdResult, Storage};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Dispute {
    id: String,
    claimant: Addr,
    respondent: Addr,
    claim: String,
    amount: Uint128,
    resolution: Option<Resolution>,
    resolved: bool,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Resolver {
    id: Addr,
    // Additional data per resolver...
}

pub const DISPUTES: Map<String, Dispute> = Map::new("disputes");
pub const RESOLVERS: Item<Resolver> = Item::new("resolvers");

// Functions to manipulate disputes and resolvers...