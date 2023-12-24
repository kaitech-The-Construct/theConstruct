use cosmwasm_std::{Addr, StdResult, Storage};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
    pub owner: Addr,
}

pub const STATE: Item<State> = Item::new("state");


#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct ManufacturingProcess {
    pub order_id: String,
    pub customer_addr:Addr,
    pub manufacturer_addr:Addr,
    pub status: OrderStatus,
}

impl ManufacturingProcess {
    pub fn new(order_id: String, customer_addr: Addr, manufacturer_addr: Addr) -> Self {
        Self {
            order_id,
            customer_addr,
            manufacturer_addr,
            status: OrderStatus::Created,
        }
    }
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub enum OrderStatus {
    Created,
    InProgress,
    Completed,
    Shipped,
    Cancelled,
}


pub const PROCESSES: Map<&str, ManufacturingProcess> = Map::new("processes");

// Helper functions using cw-storage-plus
pub fn save_state(storage: &mut dyn Storage, state: &State) -> StdResult<()> {
    STATE.save(storage, state)
}

pub fn load_state(storage: &dyn Storage) -> StdResult<State> {
    STATE.load(storage)
}

pub fn save_process(storage: &mut dyn Storage, order_id: &str, order: &ManufacturingProcess) -> StdResult<()> {
    PROCESSES.save(storage, order_id, order)
}

pub fn load_process(storage: &dyn Storage, order_id: &str) -> StdResult<ManufacturingProcess> {
    PROCESSES.load(storage, order_id)
}