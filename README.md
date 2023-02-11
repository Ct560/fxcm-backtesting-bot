# fxcm-backtesting-bot
An automatic strategy backtesting repository built on the fxcmpy API wrapper for the FXCM broker.

## Motivation:
This project exists for four main reasons: 
  1. A practical example to motivate teaching myself about trading and investing my own money.
  2. A project to present and imporve my python programming skills and, hopefully, a strong start to building a GitHub portfolio. 
  3. By the end it will be able to geuinely help me implement and build trading strategies.
  4. For fun. I enjoy coding as a past time and this is a great way to fill my weekends!

## What's Contained:
At present contains a 'codebase.py' script which will lay out the functional backbone of the bot. This will be where indicators can be definied and implemented.

The repo also contains a 'backtestFramework.py' script, which introduces the class structure for employing strategies an indicators. The approach here is to define
instances of an indicator object as some indicator function and conditions on that indicator 
(some composition of '<', '<=', '>', '>=', '==' or state based: indicator(parameters) == state_n). Then you realise a strategy object as the child-class of precisely its
constituent parent indicator objects. You could think of the strategy object as the intersection of the indicator objects. 

Looking forward I wish to implement a GUI allowing the user to build strategies from existing indicators and test them. 
