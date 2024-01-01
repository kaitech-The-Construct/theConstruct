use cosmwasm_std::{Addr, Coin};
use cosmwasm_std::{StdResult, Storage};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
    pub owner: Addr,
}

pub const STATE: Item<State> = Item::new("state");
pub const LISTINGS: Map<u64, Listing> = Map::new("listings");

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Listing {
    pub listing_id: u64,
    pub seller: Addr,
    pub token_id: String,
    pub prices: Vec<Coin>,
    pub quantity: u64,
}

// Helper functions using cw-storage-plus
pub fn save_state(storage: &mut dyn Storage, state: &State) -> StdResult<()> {
    STATE.save(storage, state)
}

pub fn load_state(storage: &dyn Storage) -> StdResult<State> {
    STATE.load(storage)
}

pub fn save_listing(storage: &mut dyn Storage, id: u64, listing: &Listing) -> StdResult<()> {
    LISTINGS.save(storage, id, listing)
}

pub fn load_listing(storage: &dyn Storage, id: u64) -> StdResult<Listing> {
    LISTINGS.load(storage, id)
}

pub fn remove_listing(storage: &mut dyn Storage, id: u64) {
    LISTINGS.remove(storage, id)
}