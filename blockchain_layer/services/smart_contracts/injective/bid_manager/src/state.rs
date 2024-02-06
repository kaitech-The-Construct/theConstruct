use cosmwasm_std::{Addr, Uint128, Storage, StdResult};
use cw_storage_plus::Item;
use cw_storage_plus::Map;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Config {
    pub owner: Addr,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Bid {
    pub bidder: Addr,
    pub amount: Uint128,
}

pub const CONFIG: Item<Config> = Item::new("config");
pub const BIDS: Map<String, Bid> = Map::new("bids");

pub fn save_bid(storage: &mut dyn Storage, order_id: &str, bid: &Bid) -> StdResult<()> {
    BIDS.save(storage, order_id, bid)
}

pub fn load_bid(storage: &dyn Storage, order_id: &str) -> StdResult<Bid> {
    BIDS.load(storage, order_id)
}