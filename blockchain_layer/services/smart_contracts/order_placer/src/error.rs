use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("Standard error: {0}")]
    Std(#[from] StdError),

    #[error("Unauthorized")]
    Unauthorized,

    #[error("Order already exists")]
    OrderAlreadyExists,

    #[error("Order not found")]
    OrderNotFound,

    #[error("Insufficient funds sent")]
    InsufficientFundsSent,

    #[error("Invalid deadline")]
    InvalidDeadline,

    #[error("Invalid input: {0}")]
    InvalidInput(String),
}