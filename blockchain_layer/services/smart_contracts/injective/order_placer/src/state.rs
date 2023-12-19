use cosmwasm_std::Addr;
use cosmwasm_std::{StdResult, Storage};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
    pub owner: Addr,
}

pub const STATE: Item<State> = Item::new("state");

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Order {
    pub id: String,
    pub creator: String,
    pub product_specification: String,
    pub quantity: u64,
    pub deadline: u64,
    pub status: OrderStatus,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub enum OrderStatus {
    Open,
    InProgress,
    Completed,
    Disputed,
}

pub const ORDERS: Map<&str, Order> = Map::new("orders");

// State and Order use `Item` as they are single, for multiple items, consider using `Map`.

// Helper functions using cw-storage-plus
pub fn save_state(storage: &mut dyn Storage, state: &State) -> StdResult<()> {
    STATE.save(storage, state)
}

pub fn load_state(storage: &dyn Storage) -> StdResult<State> {
    STATE.load(storage)
}

pub fn save_order(storage: &mut dyn Storage, id: &str, order: &Order) -> StdResult<()> {
    ORDERS.save(storage, id, order)
}

pub fn load_order(storage: &dyn Storage, id: &str) -> StdResult<Order> {
    ORDERS.load(storage, id)
}
