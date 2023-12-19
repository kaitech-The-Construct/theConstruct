use cosmwasm_std::{Addr, Coin,Timestamp, Storage, StdResult};
use cw_storage_plus::{Item, Map};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
    pub owner: Addr,
}

pub const STATE: Item<State> = Item::new("state");
pub const ESCROW_SEQUENCE: Item<u64> = Item::new("escrow_sequence");
pub const ESCROW_STATE: Map<&str, Escrow> = Map::new("escrow_state");

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Escrow {
    pub id: String,
    pub payer: Addr,
    pub beneficiary: Addr,
    pub funds: Vec<Coin>,
    pub end_time: Timestamp,
    pub released: bool,
}

pub fn save_state(storage: &mut dyn Storage, state: &State) -> StdResult<()> {
    STATE.save(storage, state)
}

pub fn load_state(storage: &dyn Storage) -> StdResult<State> {
    STATE.load(storage)
}

pub fn save_escrow(storage: &mut dyn Storage, id: &str, escrow:&Escrow) -> StdResult<()> {
    ESCROW_STATE.save(storage, id,escrow)
}

pub fn load_escrow(storage: &dyn Storage, id: &str) -> StdResult<Escrow> {
    ESCROW_STATE.load(storage, id)
}