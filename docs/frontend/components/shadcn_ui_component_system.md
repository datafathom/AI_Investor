# shadcn/ui Component System — Architecture & Patterns

> **Last Updated**: 2026-02-14
> **Location**: `Frontend/src/components/ui/`
> **Dependencies**: `@radix-ui/*`, `clsx`, `tailwind-merge`, `lucide-react`

## Overview

The Sovereign OS frontend uses the **shadcn/ui** component pattern — a set of beautifully designed, accessible, and customizable components built on top of [Radix UI](https://www.radix-ui.com/) primitives. These are **not** installed from npm as a package; they are **source-owned** components that live directly in the codebase at `Frontend/src/components/ui/`.

This design decision is intentional: it gives the team full control over styling, behavior, and accessibility without being locked into a third-party component library's release cycle.

## The `cn()` Utility — Class Name Merging

All UI components use a shared utility function defined in `Frontend/src/lib/utils.js`:

```javascript
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
```

### Why This Exists

When composing Tailwind CSS classes, conflicts can arise (e.g., `bg-red-500 bg-blue-500`). The `cn()` function:

1. **`clsx`** — Conditionally joins class names, handling arrays, objects, and falsy values
2. **`twMerge`** — Intelligently resolves Tailwind CSS class conflicts (later classes win)

This allows consumers to pass custom `className` props that properly override defaults:

```jsx
// The component's default is bg-slate-950, but this call overrides it to bg-red-900
<Card className="bg-red-900" />
```

## Component Anatomy — The Standard Pattern

Every shadcn/ui component in our codebase follows this exact pattern:

```jsx
import * as React from "react"
import * as PrimitiveName from "@radix-ui/react-primitive-name"
import { cn } from "@/lib/utils"

const ComponentName = React.forwardRef(({ className, ...props }, ref) => (
  <PrimitiveName.Root
    ref={ref}
    className={cn(
      "default tailwind classes here",
      className  // consumer overrides
    )}
    {...props}
  />
))
ComponentName.displayName = PrimitiveName.Root.displayName

export { ComponentName }
```

### Key Elements

| Element | Purpose |
|---------|---------|
| `React.forwardRef` | Allows parent components to attach refs for DOM access and focus management |
| `@radix-ui/*` primitives | Provide accessibility (ARIA), keyboard navigation, and state management out of the box |
| `cn()` | Merges default styles with consumer-provided `className` overrides |
| `displayName` | Enables React DevTools identification for debugging |
| `...props` spread | Passes through all native HTML/ARIA attributes |

## Component Inventory

The following components exist in `Frontend/src/components/ui/`:

### Radix UI Primitive-Based Components

These components wrap `@radix-ui/*` primitives and inherit full accessibility, keyboard navigation, and state management:

| Component | File | Radix Package | Exports |
|-----------|------|---------------|---------|
| **AlertDialog** | `alert-dialog.jsx` | `@radix-ui/react-alert-dialog` | `AlertDialog`, `AlertDialogTrigger`, `AlertDialogContent`, `AlertDialogHeader`, `AlertDialogFooter`, `AlertDialogTitle`, `AlertDialogDescription`, `AlertDialogAction`, `AlertDialogCancel`, `AlertDialogPortal`, `AlertDialogOverlay` |
| **Avatar** | `avatar.jsx` | `@radix-ui/react-avatar` | `Avatar`, `AvatarImage`, `AvatarFallback` |
| **Dialog** | `dialog.jsx` | `@radix-ui/react-dialog` | `Dialog`, `DialogTrigger`, `DialogContent`, `DialogHeader`, `DialogFooter`, `DialogTitle`, `DialogDescription`, `DialogClose`, `DialogPortal`, `DialogOverlay` |
| **ScrollArea** | `scroll-area.jsx` | `@radix-ui/react-scroll-area` | `ScrollArea`, `ScrollBar` |
| **Select** | `select.jsx` | `@radix-ui/react-select` | `Select`, `SelectGroup`, `SelectValue`, `SelectTrigger`, `SelectContent`, `SelectLabel`, `SelectItem`, `SelectSeparator`, `SelectScrollUpButton`, `SelectScrollDownButton` |
| **Slider** | `slider.jsx` | `@radix-ui/react-slider` | `Slider` |
| **Switch** | `switch.jsx` | `@radix-ui/react-switch` | `Switch` |

### Native HTML-Based Components

These components use native HTML elements with consistent styling, without a Radix primitive:

| Component | File | Exports |
|-----------|------|---------|
| **Alert** | `alert.jsx` | `Alert`, `AlertTitle`, `AlertDescription` |
| **Badge** | `badge.jsx` | `Badge` |
| **Button** | `button.jsx` | `Button` (default + named) |
| **Card** | `card.jsx` | `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` |
| **Input** | `input.jsx` | `Input` |
| **Label** | `label.jsx` | `Label` |
| **Progress** | `progress.jsx` | `Progress` |
| **Table** | `table.jsx` | `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell` |
| **Tabs** | `tabs.jsx` | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` |
| **Tooltip** | `tooltip.jsx` | `Tooltip`, `TooltipTrigger`, `TooltipContent`, `TooltipProvider` |

### Hooks

| Hook | File | Purpose |
|------|------|---------|
| **useToast** | `use-toast.js` | Toast notification state management |

## Import Convention

All UI components are imported via the `@/components/ui/` alias (configured in `vite.config.js` as `@ → ./src`):

```javascript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
```

### Critical Import Rules

1. **Always use the `@/` alias** — never relative paths for UI components
2. **Named exports only** — components use `export { ComponentName }`, not `export default`
3. **Exception**: `Button` has both named and default exports for backward compatibility

## Dark Theme Design Tokens

All components use a consistent dark theme palette:

| Token | Tailwind Class | Usage |
|-------|---------------|-------|
| Background | `bg-slate-950` | Primary surface |
| Border | `border-slate-800` | Component borders |
| Text | `text-slate-50` | Primary text |
| Muted text | `text-slate-400` | Secondary/descriptive text |
| Focus ring | `ring-slate-300` | Keyboard focus indicator |
| Ring offset | `ring-offset-slate-950` | Focus ring offset background |
| Hover | `bg-slate-800` | Interactive hover state |

## Adding New Components

When adding a new shadcn/ui component:

1. **Check [shadcn/ui registry](https://ui.shadcn.com/)** for the reference implementation
2. **Install the Radix primitive** if needed: `npm install @radix-ui/react-<name>`
3. **Create the file** in `Frontend/src/components/ui/<name>.jsx`
4. **Follow the standard pattern** above with `forwardRef`, `cn()`, and dark theme tokens
5. **Set `displayName`** for React DevTools
6. **Use named exports** — no default exports
7. **Update this documentation** with the new component

### Common Pitfalls

- **Do NOT create stub/placeholder components** — every component must be a complete, fully functional implementation with proper accessibility
- **Do NOT use `export default`** — the shadcn/ui convention is named exports only (except `Button` which has both for legacy reasons)
- **Do NOT hardcode colors** — always use the design tokens above so themes remain consistent
- **Do NOT skip `forwardRef`** — components must support ref forwarding for focus management and composition

## Installed Radix UI Packages

The following `@radix-ui/*` packages are currently in `package.json`:

```
@radix-ui/react-alert-dialog
@radix-ui/react-avatar
@radix-ui/react-dialog
@radix-ui/react-scroll-area
@radix-ui/react-select
@radix-ui/react-slider
@radix-ui/react-switch
```

### Not Yet Installed (may be needed for future components)

```
@radix-ui/react-accordion
@radix-ui/react-checkbox
@radix-ui/react-collapsible
@radix-ui/react-context-menu
@radix-ui/react-dropdown-menu
@radix-ui/react-hover-card
@radix-ui/react-label
@radix-ui/react-menubar
@radix-ui/react-navigation-menu
@radix-ui/react-popover
@radix-ui/react-progress
@radix-ui/react-radio-group
@radix-ui/react-separator
@radix-ui/react-toast
@radix-ui/react-toggle
@radix-ui/react-toggle-group
@radix-ui/react-toolbar
@radix-ui/react-tooltip
```
