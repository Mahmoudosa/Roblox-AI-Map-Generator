local ReplicatedStorage = game:GetService("ReplicatedStorage")
local generateEvent = ReplicatedStorage:WaitForChild("GenerateMap")
local HttpService = game:GetService("HttpService")

local materialMap = {
	Grass = Enum.Material.Grass,
	Wood = Enum.Material.Wood,
	Concrete = Enum.Material.Concrete,
	SmoothPlastic = Enum.Material.SmoothPlastic,
	Stone = Enum.Material.SmoothPlastic,
	Brick = Enum.Material.Brick,
	Sand = Enum.Material.Sand,
	Ground = Enum.Material.Ground,
	Rock = Enum.Material.SmoothPlastic,
	Marble = Enum.Material.Marble,
	Granite = Enum.Material.Granite,
	Ice = Enum.Material.Ice,
	Snow = Enum.Material.Snow,
	Metal = Enum.Material.Metal,
	Cobblestone = Enum.Material.Cobblestone,
	Fabric = Enum.Material.Fabric,
	DiamondPlate = Enum.Material.DiamondPlate,
	Dirt = Enum.Material.Ground,
	Leaves = Enum.Material.Grass,
	Water = Enum.Material.SmoothPlastic,
	Roof = Enum.Material.SmoothPlastic,
}

generateEvent.OnServerEvent:Connect(function(player, description)
	local url = "your ngrok url/generate"
	local body = HttpService:JSONEncode({description = description})
	local success, result = pcall(function()
		return HttpService:PostAsync(url, body)
	end)
	if not success then
		warn("HTTP Request Failed: " .. tostring(result))
		return
	end
	local data = HttpService:JSONDecode(result)
	local parts = HttpService:JSONDecode(data.response)
	for _, v in pairs(parts) do
		if v.position and v.size and v.color then
			local part = Instance.new("Part")
			part.Parent = workspace
			part.Size = Vector3.new(v.size[1], v.size[2], v.size[3])
			part.Position = Vector3.new(v.position[1], v.position[2], v.position[3])
			part.Color = Color3.fromRGB(v.color[1], v.color[2], v.color[3])
			part.Anchored = v.anchored ~= nil and v.anchored or true
			part.CanCollide = v.canCollide ~= nil and v.canCollide or true
			if v.material then
				part.Material = materialMap[v.material] or Enum.Material.SmoothPlastic
			end
			if v.shape then
				part.Shape = Enum.PartType[v.shape] or Enum.PartType.Block
			end
			if v.transparency then
				part.Transparency = v.transparency
			end
		else
			warn("Skipping part due to missing data")
		end
	end
end)
