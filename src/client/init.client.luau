local ContextActionService = game:GetService("ContextActionService")

local function onPrintAction(actionName: string, inputState: Enum.UserInputState, inputObject)
    if inputState == Enum.UserInputState.Begin then
        print("Player pressed the button!")
    end
end

ContextActionService:BindAction("PrintMessageAction", onPrintAction, false, Enum.KeyCode.P)

print("Client input handler initialized.")
