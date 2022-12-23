local signal = require("posix.signal")
local socket = require("socket")
local string = require("string")

local s = socket.tcp()
s:bind('0.0.0.0', 62372)
s:connect('0.0.0.0', 10800)
local index, err, lastindex = s:send([[123]])
print('index: ', index, 'err: ', err, 'lastindex: ', lastindex)
