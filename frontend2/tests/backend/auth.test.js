/**
 * Authentication Backend Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

// Mock database - create chainable mock objects
const createInsertMock = () => {
  const valuesFn = vi.fn().mockResolvedValue({});
  return {
    values: valuesFn,
  };
};

const mockDb = {
  query: {
    users: {
      findFirst: vi.fn(),
      findMany: vi.fn(),
    },
  },
  insert: vi.fn(() => createInsertMock()),
};

// Mock auth functions
const registerUser = async (username, password) => {
  const existing = await mockDb.query.users.findFirst({
    where: (users, { eq }) => eq(users.username, username),
  });

  if (existing) {
    throw new Error('User already exists');
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  const insertResult = mockDb.insert(mockDb.query.users);
  await insertResult.values({
    username,
    password: hashedPassword,
  });

  return { username };
};

const loginUser = async (username, password) => {
  const user = await mockDb.query.users.findFirst({
    where: (users, { eq }) => eq(users.username, username),
  });

  if (!user) {
    throw new Error('Invalid credentials');
  }

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) {
    throw new Error('Invalid credentials');
  }

  const token = jwt.sign({ userId: user.id, username: user.username }, 'secret');
  return { token, user: { id: user.id, username: user.username } };
};

describe('Authentication', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Re-setup the insert mock after clearing
    mockDb.insert.mockImplementation(() => createInsertMock());
  });

  describe('registerUser', () => {
    it('should register a new user', async () => {
      mockDb.query.users.findFirst.mockResolvedValue(null);
      // insert mock is already set up to return chainable object

      const result = await registerUser('testuser', 'password123');

      expect(result.username).toBe('testuser');
      expect(mockDb.insert).toHaveBeenCalled();
    });

    it('should throw error if user exists', async () => {
      mockDb.query.users.findFirst.mockResolvedValue({ id: 1, username: 'testuser' });

      await expect(registerUser('testuser', 'password123')).rejects.toThrow(
        'User already exists'
      );
    });
  });

  describe('loginUser', () => {
    it('should login with valid credentials', async () => {
      const hashedPassword = await bcrypt.hash('password123', 10);
      mockDb.query.users.findFirst.mockResolvedValue({
        id: 1,
        username: 'testuser',
        password: hashedPassword,
      });

      const result = await loginUser('testuser', 'password123');

      expect(result.token).toBeDefined();
      expect(result.user.username).toBe('testuser');
    });

    it('should throw error with invalid username', async () => {
      mockDb.query.users.findFirst.mockResolvedValue(null);

      await expect(loginUser('invalid', 'password123')).rejects.toThrow(
        'Invalid credentials'
      );
    });

    it('should throw error with invalid password', async () => {
      const hashedPassword = await bcrypt.hash('password123', 10);
      mockDb.query.users.findFirst.mockResolvedValue({
        id: 1,
        username: 'testuser',
        password: hashedPassword,
      });

      await expect(loginUser('testuser', 'wrongpassword')).rejects.toThrow(
        'Invalid credentials'
      );
    });
  });
});

