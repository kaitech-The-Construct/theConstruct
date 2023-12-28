import { SecretManagerServiceClient } from "@google-cloud/secret-manager";

// Function to access secret from GCP Secrets Manager
 export async function getSecret(name: string): Promise<string> {
  const project_id = process.env.PROJECTID || "";
  const secret_name = `projects/${project_id}/secrets/${name}/versions/latest`;

  const client = new SecretManagerServiceClient();
  try {
    const [version] = await client.accessSecretVersion({
      name: secret_name,
    });

    // Decode payload and convert to a string
    const secretData = version.payload?.data?.toString();

    if (secretData) {
      return secretData;
    } else {
      return '';
    }
  } catch (err) {
    console.error(`Error getting secret: ${err}`);
    throw new Error(`Error getting secret: ${err}`);
  }
}
