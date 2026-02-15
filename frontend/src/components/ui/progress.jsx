import * as React from "react"
import { cn } from "@/lib/utils"

const Progress = React.forwardRef(({ className, value = 0, max = 100, ...props }, ref) => (
  <div
    ref={ref}
    role="progressbar"
    aria-valuemin={0}
    aria-valuemax={max}
    aria-valuenow={value}
    className={cn(
      "relative h-4 w-full overflow-hidden rounded-full bg-slate-800",
      className
    )}
    {...props}
  >
    <div
      className="h-full w-full flex-1 bg-slate-50 transition-all duration-300 ease-in-out"
      style={{ transform: `translateX(-${100 - (value / max) * 100}%)` }}
    />
  </div>
))
Progress.displayName = "Progress"

export { Progress }
