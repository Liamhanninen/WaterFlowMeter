# WaterFlowMeter
Usinga YF-201 Water Flow Sensor track water usage and send to database.

## About
I have a 200 gallon water tank that I refill from a well when it gets low. Using this sensor I can monitor usage and know when it's time to refill the tank.

## Wiring
I used the wiring from this video https://youtu.be/wpenAP8gN3c. You can skip to 10:44 where there are a few screenshots of the wiring. I did not have to make any changes for wiring. 

## Summary of the Code
When testing I found that my estimates for any unit of volume and rate was different than in production. What I mean is that the volume per sencond of water that passed through when using a funnel w/ a water bottle was slightly different than when I plugged it into my tank. Not very surprising. So note the value of a cup in the code and perform your own calibrations in production to get the right reading.

It turns out that a rotation is signaled by sending whatever the alternate to the current state is - for example if the input is a 1 at resting then the very first rotation will be a 0. As the water continues to flow the signal continues to alternate for each rotation.

If the database insert/connection was not successful it stores the data in a list until the next attempt.

The code itself is heavily commented - good luck!
