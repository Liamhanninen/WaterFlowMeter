# WaterFlowMeter
Using a YF-201 Water Flow Sensor track water usage and send to database https://www.adafruit.com/product/828. See 'Stuff' section at the end to see everything I used.

## About
I have a 200 gallon water tank that I refill from a well when it gets low. Using this sensor I can monitor usage and know when it's time to refill the tank.

## Wiring
I used the wiring from this video https://youtu.be/wpenAP8gN3c. You can skip to 10:44 where there are a few screenshots of the wiring. I did not have to make any changes for wiring. 

## Summary of the Code
When testing I found that my estimates for any unit of volume and rate was different than in production. What I mean is that the volume per second that passed through when using a funnel w/ a water bottle was slightly different than when I plugged it into my tank. Not very surprising. So note the value of a cup in the code (cup_movements) and perform your own calibrations in production to get the right reading.

It turns out that a rotation is signaled by sending whatever the alternate to the current state is - for example if the current input is a 1 at rest then the very first rotation will be a 0. As the water continues to flow the signal continues to alternate from 1 to 0 for each rotation. Resting state can be a 1 or 0.

If the database insert/connection was not successful it stores the data in a list until the next attempt.

The code itself is heavily commented - good luck!

## Getting Started

`git clone https://github.com/Liamhanninen/WaterFlowMeter.git`

`cd WaterFlowMeter`

`pip install -r requirements.txt`

`python water_flow.py`

## Stuff
0. Raspberry Pi Zero WH (Zero W with Headers) (headers optional) https://www.adafruit.com/product/3708?gclid=CjwKCAiAzanuBRAZEiwA5yf4ul30H_1a7R2wLFtjlCfOP4aGevPwQkN8Vo97Pvj_m4r_UZRgzIpz6RoCd7AQAvD_BwE
1. YF-201 Water Flow Sensor https://www.adafruit.com/product/828
2. 4.7k resistor https://www.amazon.com/Elegoo-Values-Resistor-Assortment-Compliant/dp/B072BL2VX1/ref=sr_1_1_sspa?crid=2H58UQTN5WJB9&keywords=resistor+kit&qid=1573608352&sprefix=resistor%2Caps%2C303&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFGQ1FQOTdNQ0lEQUImZW5jcnlwdGVkSWQ9QTA2NDkzNjcxWERXWVFaUEFRS0s2JmVuY3J5cHRlZEFkSWQ9QTA2NTc0MDVIRFVIVUk3UzFGSDEmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl
3. 10k resistor (see link in #2)
4. Blue Monster Pipe Sealent tape (any sealent tape works) https://www.menards.com/main/plumbing/plumbing-installation-repair/pipe-sealants-caulk-putty/blue-monster-1-2-x-1429-pipe-thread-tape/70885/p-1444440441022-c-8531.htm?tid=-817058810073155805&ipos=10
5. Male adapter to garden hose https://www.menards.com/main/plumbing/rough-plumbing/pipe-tubing-hoses-fittings-accessories/fittings/garden-hose-fittings/sioux-chief-3-4-male-garden-hose-x-1-2-fip-brass-adapter/0122223/p-1444442661694-c-9432.htm?searchTermToProduct=0122223
6. Female adapter to garden hose https://www.menards.com/main/plumbing/rough-plumbing/pipe-tubing-hoses-fittings-accessories/fittings/garden-hose-fittings/sioux-chief-3-4-female-garden-hose-x-1-2-fip-brass-adapter/0122025/p-1444442656386-c-9432.htm?searchTermToProduct=0122025
7. Obviously also some wire, hose and patience.

Good luck!

