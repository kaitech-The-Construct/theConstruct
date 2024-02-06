use cosmwasm_std::{Addr, Coin, StdResult, Storage};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
    pub owner: Addr,
}

pub const STATE: Item<State> = Item::new("state");
pub const LISTINGS: Map<String, Listing> = Map::new("listings");
pub const OFFERS: Map<String, Vec<Offer>> = Map::new("offers");
pub const TRANSACTIONS: Map<String, Transaction> = Map::new("transactions");
pub const DISPUTES: Map<String, Dispute> = Map::new("disputes");
pub const PLATFORM_STATISTICS: Item<Statistics> = Item::new("statistics");
pub const SELLER_RATINGS: Map<Addr, Vec<Rating>> = Map::new("ratings");

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Listing {
    pub listing_id: String,
    pub seller: Addr,
    pub token_id: String,
    pub prices: Vec<Coin>,
    pub quantity: u64,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Offer {
    pub offer_id: String,
    pub buyer: Addr,
    pub price: Coin,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Transaction {
    pub transaction_id: String,
    // Include details relevant to transactions
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Dispute {
    pub dispute_id: String,
    // Include details relevant to disputes
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Statistics {
    // Include fields relevant to platform statistics
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Rating {
    pub rating_id: String,
    pub rating_value: u8,
    // Include details relevant to seller ratings
}

// Update helper functions to include new storage maps 
pub fn save_state(storage: &mut dyn Storage, state: &State) -> StdResult<()> {
    STATE.save(storage, state)
}

pub fn load_state(storage: &dyn Storage) -> StdResult<State> {
    STATE.load(storage)
}

pub fn save_listing(storage: &mut dyn Storage, id: String, listing: &Listing) -> StdResult<()> {
    LISTINGS.save(storage, &id, listing)
}

pub fn load_listing(storage: &dyn Storage, id: String) -> StdResult<Listing> {
    LISTINGS.load(storage, &id)
}

pub fn remove_listing(storage: &mut dyn Storage, id: String) {
    LISTINGS.remove(storage, &id)
}

// Add new helper functions for additional structs
// ...

// These functions will handle saving, loading, and removing data from their respective storage maps.
// Omitted for brevity, implement functions for offers, disputes, transactions, and ratings.