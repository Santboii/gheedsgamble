import { sql } from '@vercel/postgres';

export { sql };

// Helper to get or create user
export async function getOrCreateUser(email: string, name?: string, image?: string) {
    const userId = email; // Use email as ID for simplicity

    // Try to get existing user
    const existingUser = await sql`
    SELECT * FROM users WHERE id = ${userId}
  `;

    if (existingUser.rows.length > 0) {
        return existingUser.rows[0];
    }

    // Create new user
    const newUser = await sql`
    INSERT INTO users (id, email, name, image)
    VALUES (${userId}, ${email}, ${name || null}, ${image || null})
    RETURNING *
  `;

    return newUser.rows[0];
}
