local ReplicatedStorage = game:GetService("ReplicatedStorage")
local generateEvent = ReplicatedStorage:WaitForChild("GenerateMap")

local frame = script.Parent
local textbox = frame.TextBox
local button = frame.TextButton
local label = frame.TextLabel

button.MouseButton1Click:Connect(function()
	label.Text = "Generating..."
	generateEvent:FireServer(textbox.Text)
	
end)
