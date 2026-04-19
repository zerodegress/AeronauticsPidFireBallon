-- SPDX-License-Identifier: GPL-3.0-or-later
-- Copyright (C) 2026 zerodegress

local ToTheSky = {}

local Pid = {}

function Pid.createPid(kp, ki, kd, tick, u)
    local pid = {
        k = 0,
        u = u,
        e = {},
    }

    function pid:step(err)
        self.e[self.k] = err
        if self.k == 0 then
            self.e[-1] = 0.
            self.e[-2] = 0.
        end
        local du = kp * (self.e[self.k] - self.e[self.k - 1]) + ki * tick * self.e[self.k] +
            kd * (self.e[self.k] - 2 * self.e[self.k - 1] + self.e[self.k - 2]) / tick
        self.u = self.u + du
        self.k = self.k + 1
        return self.u
    end

    return pid
end

ToTheSky.pid = Pid

return ToTheSky
