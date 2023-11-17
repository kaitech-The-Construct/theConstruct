// Import required Solana libraries
use solana_program::{
    account_info::next_account_info,
    account_info::AccountInfo,
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    program_error::ProgramError,
    pubkey::Pubkey,
    sysvar::{rent::Rent, Sysvar},
};

// Define the data structure for an Invoice
#[derive(Debug)]
struct Invoice {
    provider: Pubkey,      // Service provider's public key
    user: Pubkey,          // User's public key
    amount: u64,           // Invoice amount in lamports
    is_paid: bool,         // Flag to indicate if the invoice is paid
}

// Define the program entrypoint
entrypoint!(process_instruction);

fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    _instruction_data: &[u8],
) -> ProgramResult {
    // Extract accounts
    let accounts_iter = &mut accounts.iter();
    let provider_account = next_account_info(accounts_iter)?;
    let user_account = next_account_info(accounts_iter)?;

    // Ensure that the program's instruction is signed by the provider
    if !provider_account.is_signer {
        msg!("Provider account must sign the instruction");
        return Err(ProgramError::MissingRequiredSignature);
    }

    // Create a unique seed for the invoice account
    let seed = b"invoice";
    let invoice_account = Pubkey::create_with_seed(provider_account.key, seed, program_id)?;

    // Load the rent sysvar to check if the invoice account can be created
    let rent = Rent::get()?;
    if !rent.is_exempt(provider_account.lamports(), invoice_account.to_string()) {
        msg!("Provider does not have enough lamports for invoice creation");
        return Err(ProgramError::InsufficientFunds);
    }

    // Create the invoice account
    solana_program::system_program::create_account(
        provider_account,
        &invoice_account,
        1_000_000,  // Initial lamport balance for the invoice account
        0,          // Account size (can be adjusted as needed)
        program_id,
    )?;

    // Initialize the invoice data
    let mut invoice_data = Invoice {
        provider: *provider_account.key,
        user: *user_account.key,
        amount: 0,          // Initialize with zero lamports
        is_paid: false,     // The invoice is initially unpaid
    };

    // Serialize and store the invoice data in the invoice account
    let data = bincode::serialize(&invoice_data)?;
    let mut invoice_account_data = invoice_account.try_borrow_mut_data()?;
    invoice_account_data[..data.len()].copy_from_slice(&data);

    msg!("Invoice created successfully");

    Ok(())
}

// Entry point of the program
solana_program::declare_id!("Invoice1111111111111111111111111111111111111");
