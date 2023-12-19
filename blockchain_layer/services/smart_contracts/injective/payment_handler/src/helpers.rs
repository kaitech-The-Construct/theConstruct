// If used to abstract validation logic from the `execute` function

use cosmwasm_std::{Addr, Api, StdResult, StdError};


// Validates if a beneficiary address exists and is in the correct format.
pub fn validate_beneficiary_address(api: &dyn Api, beneficiary: &str) -> StdResult<Addr> {
    api.addr_validate(beneficiary).map_err(|_| StdError::generic_err("Invalid beneficiary address"))
}