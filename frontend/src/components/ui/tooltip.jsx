import * as React from "react"
import { cn } from "@/lib/utils"

const TooltipProvider = ({ children, delayDuration = 200, ...props }) => (
  <>{children}</>
)

const TooltipContext = React.createContext({ open: false, setOpen: () => {} })

const Tooltip = ({ children, open: controlledOpen, onOpenChange, defaultOpen = false }) => {
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen)
  const open = controlledOpen !== undefined ? controlledOpen : internalOpen
  const setOpen = onOpenChange || setInternalOpen

  return (
    <TooltipContext.Provider value={{ open, setOpen }}>
      <div className="relative inline-flex">{children}</div>
    </TooltipContext.Provider>
  )
}

const TooltipTrigger = React.forwardRef(({ className, asChild, children, ...props }, ref) => {
  const { setOpen } = React.useContext(TooltipContext)

  return (
    <div
      ref={ref}
      className={cn("inline-flex", className)}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)}
      onBlur={() => setOpen(false)}
      {...props}
    >
      {children}
    </div>
  )
})
TooltipTrigger.displayName = "TooltipTrigger"

const TooltipContent = React.forwardRef(({ className, sideOffset = 4, children, side = "top", ...props }, ref) => {
  const { open } = React.useContext(TooltipContext)

  if (!open) return null

  const sideStyles = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2",
  }

  return (
    <div
      ref={ref}
      className={cn(
        "absolute z-50 overflow-hidden rounded-md border border-slate-800 bg-slate-950 px-3 py-1.5 text-sm text-slate-50 shadow-md animate-in fade-in-0 zoom-in-95",
        sideStyles[side],
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
})
TooltipContent.displayName = "TooltipContent"

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider }
