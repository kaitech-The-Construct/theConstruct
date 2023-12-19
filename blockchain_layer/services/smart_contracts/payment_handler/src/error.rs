use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("{0}")]
    Std(#[from] StdError),

    #[error("Unauthorized")]
    Unauthorized,

    #[error("Escrow already exists with this ID")]
    EscrowAlreadyExists,

    #[error("Provided end time is not in the future")]
    InvalidEndTime,

    #[error("Escrow not found or already released")]
    EscrowNotFound,

    #[error("Escrow not yet matured for release")]
    ReleaseNotAllowed,

    // Additional custom errors for validation
    #[error("Attempt to create escrow without funds")]
    NoFundsProvided,

    #[error("Invalid beneficiary address")]
    InvalidBeneficiary

}