// Helper functions to assist with common tasks, such as price validation.

use cosmwasm_std::{Coin, Uint128};

use crate::ContractError;

// Validate pricing 
pub fn validate_price(price: Vec<Coin>) -> Result<Vec<Coin>, ContractError> {
    for coin in &price {
        if coin.amount.is_zero() || coin.amount > Uint128::zero() {
            return Err(ContractError::InvalidPrice);
        }
    }

    Ok(price)
}
