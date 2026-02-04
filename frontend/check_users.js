
import { db } from './db/index.js';
import { users } from './db/schema.js';

async function listUsers() {
    try {
        const allUsers = await db.select().from(users);
        console.log('Users found:', allUsers);
        process.exit(0);
    } catch (error) {
        console.error('Error listing users:', error);
        process.exit(1);
    }
}

listUsers();
