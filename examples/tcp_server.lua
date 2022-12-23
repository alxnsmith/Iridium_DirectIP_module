local signal = require("posix.signal")
local socket = require("socket")
local string = require("string")

local s = socket.tcp()
s:bind('0.0.0.0', 10800)
s:listen(1)
s:settimeout(10)
local client, err = s:accept(s)
local data, err, part = client:receive(1024)
print('data: ', data, 'err: ', err, 'part: ', part)


s:close()
