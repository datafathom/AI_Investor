/** @type { import("drizzle-kit").Config } */
export default {
    schema: "./db/schema.js",
    out: "./drizzle",
    dialect: 'postgresql',
    dbCredentials: {
        url: process.env.DATABASE_URL || 'postgresql://investor_user:investor_password@localhost:5432/investor_db',
    },
};
