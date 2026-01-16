/**
 * ESLint Configuration
 */

module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  plugins: ['react', 'react-hooks', 'react-refresh'],
  rules: {
    'react/react-in-jsx-scope': 'off', // Not needed in React 17+
    'react/prop-types': 'warn', // Warn about missing prop types
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'no-unused-vars': ['warn', { 
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
    }],
    'no-console': ['warn', { 
      allow: ['warn', 'error', 'info'] 
    }],
    'no-debugger': 'warn',
  },
  ignorePatterns: ['dist', 'node_modules', '*.config.js', '*.config.cjs'],
};

