use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("{0}")]
    Std(#[from] StdError),

    #[error("Unauthorized")]
    Unauthorized,

    #[error("Dispute not found")]
    DisputeNotFound,

    #[error("Dispute already resolved")]
    DisputeAlreadyResolved,

    #[error("Resolution not allowed")]
    ResolutionNotAllowed,
    
    // Add more custom errors as needed.
}