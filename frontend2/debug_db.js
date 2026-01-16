
import pg from 'pg';
const { Pool } = pg;

const connectionString = process.env.DATABASE_URL || 'postgresql://investor_user:investor_password@localhost:5432/investor_db';
console.log('Connecting to:', connectionString);

const pool = new Pool({ connectionString });

async function checkTables() {
    try {
        const client = await pool.connect();
        console.log('Connected successfully.');

        const res = await client.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        `);

        console.log('Tables in public schema:', res.rows);

        client.release();
        await pool.end();
    } catch (err) {
        console.error('Connection error:', err);
    }
}

checkTables();
