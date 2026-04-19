
local sensor = peripheral.wrap('top')
if sensor == nil then
    printError("sensor not placed")
    return
end

data = {}

while true do
    sleep(0.1)
    data[#data + 1] = sensor.getHeight()
    if #data > 1200 then
        break
    end
end


dataf = fs.open('data.json', 'w')
dataf.writeLine('[')
for index, value in ipairs(data) do
    dataf.writeLine(value .. ',')
end
dataf.writeLine(']')
dataf.close()
