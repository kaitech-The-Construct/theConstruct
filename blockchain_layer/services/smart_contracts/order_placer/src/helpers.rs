// In helpers.rs
use cosmwasm_std::{Env, Coin, Uint128};
use crate::error::ContractError;
// use cosmwasm_std::{Env, Coin, Uint128};

// pub fn validate_funds_sent(funds: Vec<Coin>, required_amount: Uint128) -> Result<(), ContractError> {
//     // Adjust the logic if you accept multiple denominations
// }

// Note: The random number generator should be replaced by a secure one if needed.
pub fn generate_order_id(env: &Env) -> String {
    let time = env.block.time.nanos();
    format!("order{}", time)
}

pub fn validate_deadline(deadline: u64, env: &Env) -> Result<(), ContractError> {
    if deadline <= env.block.time.seconds() {
        Err(ContractError::InvalidDeadline)
    } else {
        Ok(())
    }
}

pub fn validate_funds_sent(funds: &[Coin], required_amount: Uint128) -> Result<(), ContractError> {
    if funds.iter().find(|c| c.denom == "ust" && c.amount >= required_amount).is_some() {
        Ok(())
    } else {
        Err(ContractError::InsufficientFundsSent)
    }
}