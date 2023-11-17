// Import modules
use solana_program::{
    account_info::AccountInfo,
    instruction::Instruction::bincode,

    program_error::ProgramError,
    pubkey::Pubkey,
};

pub mod instruction;

// ...

// Define the process_instruction function
fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> Result<(), ProgramError> {
    // Handle other instructions (invoice creation, management) here

    // Check the instruction data to determine the type of instruction
    if instruction_data.len() == 1 && instruction_data[0] == 1 {
        // Call the payment processing function
        let instruction = bincode::deserialize(instruction_data)?;
        return instruction::process_payment(program_id, accounts, instruction);
    }

    // Handle other types of instructions if necessary

    Ok(())
}
