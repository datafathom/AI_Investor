import * as React from "react"
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Simplified Label component 
 * Avoids Radix UI dependency which is not in package.json
 */
const labelVariants = "text-sm font-medium leading-none cursor-default peer-disabled:cursor-not-allowed peer-disabled:opacity-70"

const Label = React.forwardRef(({ className, ...props }, ref) => (
  <label
    ref={ref}
    className={twMerge(labelVariants, className)}
    {...props}
  />
))
Label.displayName = "Label"

export { Label }
