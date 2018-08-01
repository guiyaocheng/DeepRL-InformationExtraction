

local env = torch.class('GameEnv')

local json = require ("dkjson")
local zmq = require "lzmq"

if pcall(require, 'signal') then
    signal.signal("SIGPIPE", function() print("raised") end)
else
    print("No signal module found. Assuming SIGPIPE is okay.")
end

function env:__init(args)

    self.ctx = zmq.context()
    self.skt = self.ctx:socket{zmq.REQ,
        linger = 0, rcvtimeo = 10000;
        --connect = "tcp://127.0.0.1:" .. args.zmq_port;
        connect = "tcp://" .. args.zmq_ip .. ":" .. args.zmq_port;
    }

    if args.mode == 'Shooter' then
        self.actions = {0,1,2,3,4,5,999} -- SHooter
        -- actions for selecting each entity or stopping
        -- Action 5 - ignore all entities
        -- Action 999 - take all entities
    elseif args.mode == 'DS' then
        self.actions = {0,1,2,3,4,999} -- Distant Supervision
    elseif args.mode == 'DS02' then
        self.actions = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 999} -- Distant Supervision model
    else
        self.actions = {0,1,2,3,4,999}  --EMA
    end

end

function env:process_msg(msg)    
    -- screen, reward, terminal
    -- print("MESSAGE:", msg)
    loadstring(msg)()
    -- if reward ~= 0 then
    --     print('non-zero reward', reward)
    -- end    
    return torch.Tensor(state), reward, terminal
end

function env:newGame()
    self.skt:send("newGame")
    msg = self.skt:recv()
    while msg == nil do
        msg = self.skt:recv()
    end
    return self:process_msg(msg)
end


function env:step(action, query)
    -- assert(action==1 or action==0, "Action " .. tostring(action))
    self.skt:send(tostring(action) .. ' ' .. tostring(query))
    msg = self.skt:recv()
    while msg == nil do
        msg = self.skt:recv()
    end
    return self:process_msg(msg)
end

function env:evalStart()
    self.skt:send("evalStart")
    msg = self.skt:recv()
    assert(msg == 'done', msg)
end

function env:evalEnd()
    self.skt:send("evalEnd")
    msg = self.skt:recv()
    assert(msg == 'done', msg)
end


function env:getActions()   
    return self.actions

end
