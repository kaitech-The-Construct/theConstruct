use solana_program::{
    account_info::{next_account_info, AccountInfo},
    program_error::ProgramError,
    pubkey::Pubkey,
    program::invoke,
};

// Define the instruction data structure for processing payments
use solana_program::system_instruction::transfer;
// Define the instruction data structure for processing payments
#[derive(Debug)]
pub struct PaymentInstruction {
    pub user: Pubkey,
    pub service_provider: Pubkey,
    pub amount: u64, // Amount to be paid in lamports
}

// Define the payment processing function
pub fn process_payment(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction: PaymentInstruction,
) -> Result<(), ProgramError> {
    // Extract accounts (provider, user, business)
    let accounts_iter = &mut accounts.iter();
    let provider_account = next_account_info(accounts_iter)?;
    let user_account = next_account_info(accounts_iter)?;
    let business_account = next_account_info(accounts_iter)?;

    // Ensure the provider account is the signer
    if !provider_account.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // Calculate the business's cut (2.5% of the amount)
    let amount = instruction.amount;
    let business_cut = amount * 25 / 1000;

    // Prepare the transfer instruction to move funds to the business
    let business_transfer = transfer(provider_account.key, business_account.key, business_cut);

    // Prepare the transfer instruction to move the remaining funds to the service provider
    let provider_transfer = transfer(provider_account.key, user_account.key, amount - business_cut);

    // Define the instructions in a batch
    let instructions = vec![business_transfer, provider_transfer];

    // Create a transaction to execute the batch of instructions
    let transaction = Transaction::new(
        provider_account,
        instructions,
        provider_account.blockhash,
    );

    // Invoke the transaction
    invoke(&transaction, accounts)?;

    Ok(())
}

