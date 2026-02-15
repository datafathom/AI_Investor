from pydantic import BaseModel, Field
from agents.tools_registry import BaseTool, get_tool_registry

class CalculatorSchema(BaseModel):
    operation: str = Field(..., pattern="^(add|subtract|multiply|divide)$", description="The operation to perform.")
    x: float = Field(..., description="First number")
    y: float = Field(..., description="Second number")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform basic arithmetic operations."
    args_schema = CalculatorSchema

    def run(self, args: CalculatorSchema) -> float:
        if args.operation == "add":
            return args.x + args.y
        elif args.operation == "subtract":
            return args.x - args.y
        elif args.operation == "multiply":
            return args.x * args.y
        elif args.operation == "divide":
            if args.y == 0:
                raise ValueError("Cannot divide by zero.")
            return args.x / args.y
        else:
            raise ValueError(f"Unknown operation: {args.operation}")

# Auto-register
get_tool_registry().register(CalculatorTool)
