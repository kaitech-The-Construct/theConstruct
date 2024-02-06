use crate::state::{Dispute, Resolver};
use cosmwasm_std::{Env};
use crate::error::ContractError;

pub fn can_dispute_be_resolved(dispute: &Dispute, resolver: &Resolver, env: &Env) -> Result<(), ContractError> {
    if dispute.resolved {
        return Err(ContractError::DisputeAlreadyResolved);
    }

    // More complex logic to validate the dispute resolution...
    Ok(())
}