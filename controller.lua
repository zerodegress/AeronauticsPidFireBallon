local tothesky = require('tothesky')
local pid = tothesky.pid

local sensor = peripheral.wrap('top')
if (sensor == nil) then
    printError("sensor not placed")
    return
end

HEIGHT = 100.

local control = pid.createPid(1., .017, 2., 0.1, redstone.getAnalogOutput('right'))

while true do
    local output = control:step(HEIGHT - sensor.getHeight())
    print(HEIGHT - sensor.getHeight())
    print(output)
    if output > 15 then
        output = 15
    elseif output < 0 then
        output = 0
    end
    output = math.floor(output)
    redstone.setAnalogOutput('right', output)
    sleep(0.1)
end
