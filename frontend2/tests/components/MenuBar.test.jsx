/**
 * MenuBar Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MenuBar from '../../src/components/MenuBar';

describe('MenuBar', () => {
  const defaultProps = {
    onMenuAction: vi.fn(),
    isDarkMode: false,
    widgetVisibility: {},
    onToggleWidget: vi.fn(),
    onTriggerModal: vi.fn(),
    onResetLayout: vi.fn(),
    toggleTheme: vi.fn(),
    onAutoSort: vi.fn(),
    onSaveLayout: vi.fn(),
    onLoadLayout: vi.fn(),
    onToggleLogCenter: vi.fn(),
    showLogCenter: false,
    debugStates: {},
    widgetTitles: {},
    currentUser: null,
    onSignin: vi.fn(),
    onLogout: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render menu bar with all menu items', () => {
    render(<MenuBar {...defaultProps} />);

    // Menu items are rendered as clickable divs with role="menuitem"
    expect(screen.getByText('File')).toBeInTheDocument();
    expect(screen.getByText('Edit')).toBeInTheDocument();
    expect(screen.getByText('View')).toBeInTheDocument();
    expect(screen.getByText('Widgets')).toBeInTheDocument();
    expect(screen.getByText('Selection')).toBeInTheDocument();
    expect(screen.getByText('Tools')).toBeInTheDocument();
    expect(screen.getByText('Help')).toBeInTheDocument();
    expect(screen.getByText('Account')).toBeInTheDocument();
  });

  it('should open dropdown menu when menu item is clicked', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} />);

    const fileMenu = screen.getByText('File');
    await user.click(fileMenu);

    await waitFor(() => {
      expect(screen.getByText('New Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Open Dashboard')).toBeInTheDocument();
      // Save Layout appears in File menu (and possibly Account menu)
      expect(screen.getAllByText('Save Layout').length).toBeGreaterThan(0);
    });
  });

  it('should call onMenuAction when menu item is clicked', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} />);

    const fileMenu = screen.getByText('File');
    await user.click(fileMenu);

    await waitFor(() => {
      expect(screen.getByText('New Dashboard')).toBeInTheDocument();
    });

    const newDashboardItem = screen.getByText('New Dashboard');
    await user.click(newDashboardItem);

    expect(defaultProps.onMenuAction).toHaveBeenCalledWith('new-dashboard');
  });

  it('should show Account menu with Sign In when user is not logged in', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} currentUser={null} />);

    const accountMenu = screen.getByText('Account');
    await user.click(accountMenu);

    await waitFor(() => {
      expect(screen.getByText(/sign in/i)).toBeInTheDocument();
    });
  });

  it('should show Account menu with user info when logged in', async () => {
    const user = userEvent.setup();
    const currentUser = { id: 1, username: 'testuser' };
    render(<MenuBar {...defaultProps} currentUser={currentUser} />);

    const accountMenu = screen.getByText('Account');
    await user.click(accountMenu);

    await waitFor(() => {
      expect(screen.getByText(/signed in as testuser/i)).toBeInTheDocument();
      expect(screen.getByText('Logout')).toBeInTheDocument();
    });
  });

  it('should call onLogout when logout is clicked', async () => {
    const user = userEvent.setup();
    const currentUser = { id: 1, username: 'testuser' };
    render(<MenuBar {...defaultProps} currentUser={currentUser} />);

    const accountMenu = screen.getByText('Account');
    await user.click(accountMenu);

    await waitFor(() => {
      expect(screen.getByText('Logout')).toBeInTheDocument();
    });

    const logoutItem = screen.getByText('Logout');
    await user.click(logoutItem);

    expect(defaultProps.onLogout).toHaveBeenCalled();
  });

  it('should call onSignin when sign in is clicked', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} currentUser={null} />);

    const accountMenu = screen.getByText('Account');
    await user.click(accountMenu);

    await waitFor(() => {
      expect(screen.getByText(/sign in/i)).toBeInTheDocument();
    });

    const signInItem = screen.getByText(/sign in/i);
    await user.click(signInItem);

    expect(defaultProps.onSignin).toHaveBeenCalled();
  });

  it('should close dropdown when clicking outside', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} />);

    const fileMenu = screen.getByText('File');
    await user.click(fileMenu);

    await waitFor(() => {
      expect(screen.getByText('New Dashboard')).toBeInTheDocument();
    });

    // Click outside
    await user.click(document.body);

    await waitFor(() => {
      expect(screen.queryByText('New Dashboard')).not.toBeInTheDocument();
    });
  });

  it('should toggle theme when theme toggle is clicked', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} />);

    const themeToggle = screen.getByRole('checkbox', { name: /toggle dark mode/i });
    await user.click(themeToggle);

    expect(defaultProps.toggleTheme).toHaveBeenCalled();
  });

  it('should display widget titles in Widgets menu', async () => {
    const user = userEvent.setup();
    const widgetTitles = {
      'api': 'API Integration',
      'docker': 'Docker Containers',
    };
    render(<MenuBar {...defaultProps} widgetTitles={widgetTitles} />);

    const widgetMenu = screen.getByText('Widgets');
    await user.click(widgetMenu);

    await waitFor(() => {
      expect(screen.getByText('API Integration')).toBeInTheDocument();
      expect(screen.getByText('Docker Containers')).toBeInTheDocument();
    });
  });

  it('should call onToggleWidget when widget menu item is clicked', async () => {
    const user = userEvent.setup();
    const widgetTitles = {
      'api': 'API Integration',
    };
    render(<MenuBar {...defaultProps} widgetTitles={widgetTitles} />);

    const widgetMenu = screen.getByText('Widgets');
    await user.click(widgetMenu);

    await waitFor(() => {
      expect(screen.getByText('API Integration')).toBeInTheDocument();
    });

    const apiWidget = screen.getByText('API Integration');
    await user.click(apiWidget);

    expect(defaultProps.onToggleWidget).toHaveBeenCalledWith('api');
  });

  it('should show checked state for visible widgets', async () => {
    const user = userEvent.setup();
    const widgetTitles = {
      'api': 'API Integration',
    };
    const widgetVisibility = {
      'api': true,
    };
    render(
      <MenuBar
        {...defaultProps}
        widgetTitles={widgetTitles}
        widgetVisibility={widgetVisibility}
      />
    );

    const widgetMenu = screen.getByText('Widgets');
    await user.click(widgetMenu);

    await waitFor(() => {
      expect(screen.getByText('API Integration')).toBeInTheDocument();
    });

    const apiWidget = screen.getByText('API Integration');
    const menuItem = apiWidget.closest('[role="menuitem"]');
    if (menuItem) {
      expect(menuItem).toHaveAttribute('aria-checked', 'true');
    } else {
      // Check if widget has checkmark
      const checkmark = apiWidget.closest('.menu-dropdown-item')?.querySelector('.menu-checkmark');
      expect(checkmark).toBeInTheDocument();
    }
  });

  it('should render action buttons in menu bar', () => {
    render(<MenuBar {...defaultProps} />);

    expect(screen.getByRole('button', { name: /auto sort/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /save layout/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /load layout/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /reset layout/i })).toBeInTheDocument();
  });

  it('should call respective handlers when action buttons are clicked', async () => {
    const user = userEvent.setup();
    render(<MenuBar {...defaultProps} />);

    const autoSortButton = screen.getByRole('button', { name: /auto sort/i });
    await user.click(autoSortButton);
    expect(defaultProps.onAutoSort).toHaveBeenCalled();

    const saveLayoutButton = screen.getByRole('button', { name: /save layout/i });
    await user.click(saveLayoutButton);
    expect(defaultProps.onSaveLayout).toHaveBeenCalled();

    const loadLayoutButton = screen.getByRole('button', { name: /load layout/i });
    await user.click(loadLayoutButton);
    expect(defaultProps.onLoadLayout).toHaveBeenCalled();

    const resetLayoutButton = screen.getByRole('button', { name: /reset layout/i });
    await user.click(resetLayoutButton);
    expect(defaultProps.onResetLayout).toHaveBeenCalled();
  });
});

