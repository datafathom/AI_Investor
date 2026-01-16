
import { db } from './db/index.js';
import { users } from './db/schema.js';
import bcrypt from 'bcryptjs';

async function registerUser() {
    try {
        const username = 'admin';
        const password = 'password123';
        const hashedPassword = await bcrypt.hash(password, 10);

        await db.insert(users).values({
            username,
            password: hashedPassword,
        });

        console.log(`User registered: ${username} / ${password}`);
        process.exit(0);
    } catch (error) {
        console.error('Registration error:', error);
        process.exit(1);
    }
}

registerUser();
