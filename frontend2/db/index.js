import { drizzle } from 'drizzle-orm/node-postgres';
import pg from 'pg';
import * as schema from './schema.js';

const { Pool } = pg;

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || 'postgresql://investor_user:investor_password@localhost:5432/investor_db',
});

export const db = drizzle(pool, { schema });
