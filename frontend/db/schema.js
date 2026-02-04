import { pgTable, text, integer, serial, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
    id: serial('id').primaryKey(),
    username: text('username').notNull().unique(),
    password: text('password').notNull(),
    createdAt: timestamp('created_at').defaultNow(),
});

export const layouts = pgTable('layouts', {
    id: serial('id').primaryKey(),
    userId: integer('user_id').references(() => users.id),
    layoutData: text('layout_data').notNull(), // JSON string
    updatedAt: timestamp('updated_at').defaultNow(),
});

export const windowLayouts = pgTable('window_layouts', {
    id: serial('id').primaryKey(),
    userId: integer('user_id').references(() => users.id),
    name: text('name').notNull(),
    layoutData: text('layout_data').notNull(), // JSON string of window configurations
    createdAt: timestamp('created_at').defaultNow(),
    updatedAt: timestamp('updated_at').defaultNow(),
});

export const roles = pgTable('roles', {
    id: serial('id').primaryKey(),
    name: text('name').notNull().unique(),
    description: text('description'),
    createdAt: timestamp('created_at').defaultNow(),
});

export const userRoles = pgTable('user_roles', {
    id: serial('id').primaryKey(),
    userId: integer('user_id').references(() => users.id).notNull(),
    roleId: integer('role_id').references(() => roles.id).notNull(),
    assignedAt: timestamp('assigned_at').defaultNow(),
});

export const permissions = pgTable('permissions', {
    id: serial('id').primaryKey(),
    name: text('name').notNull().unique(),
    resource: text('resource').notNull(), // e.g., 'widget', 'window', 'layout'
    action: text('action').notNull(), // e.g., 'read', 'write', 'delete', 'admin'
    description: text('description'),
    createdAt: timestamp('created_at').defaultNow(),
});

export const rolePermissions = pgTable('role_permissions', {
    id: serial('id').primaryKey(),
    roleId: integer('role_id').references(() => roles.id).notNull(),
    permissionId: integer('permission_id').references(() => permissions.id).notNull(),
    grantedAt: timestamp('granted_at').defaultNow(),
});

export const teams = pgTable('teams', {
    id: serial('id').primaryKey(),
    name: text('name').notNull(),
    description: text('description'),
    createdBy: integer('created_by').references(() => users.id),
    createdAt: timestamp('created_at').defaultNow(),
});

export const teamMembers = pgTable('team_members', {
    id: serial('id').primaryKey(),
    teamId: integer('team_id').references(() => teams.id).notNull(),
    userId: integer('user_id').references(() => users.id).notNull(),
    role: text('role').notNull().default('member'), // 'owner', 'admin', 'member'
    joinedAt: timestamp('joined_at').defaultNow(),
});

export const userPreferences = pgTable('user_preferences', {
    id: serial('id').primaryKey(),
    userId: integer('user_id').references(() => users.id).notNull().unique(),
    theme: text('theme').default('light'),
    layout: text('layout'), // JSON string
    notifications: text('notifications'), // JSON string
    updatedAt: timestamp('updated_at').defaultNow(),
});
