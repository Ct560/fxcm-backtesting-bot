#Code to formalise a strategy class object
#Code to be able to work with that class to test it on histroical data

'''We need a strategy config interpreter '''

class ConditionObj:
    

class IndicatorObj:
    def __init__(self, indicatorFunc, indicatorConditions):
        self.indicator_function = indicatorFunc
        self.indicator_conditions = indicatorConditions

class Strategy(IndicatorObjects):
    def __init__(self, indicatorObjects):
        self.indicators = indicatorObjects

    def __str__(self):
        return "This strategy consists of these indicators" + str(self.indicators)

    def __iter__(self):
        self.indicatorPointer = 0
        return self.indicators[0]
        
    def __next__(self):
        if self.indicatorPointer <= len(self.indicators) - 1:
            self.indicatorPointer += 1
            return self.indicators[self.indicatorPointer]
        else:
            raise StopIteration

        
'''class strategy(indicators and paramaters):
    if all buy indicators are hit at some parameters:
        buy at time t, include all costs
    if all sell indicators are hit at some parameters:
        sell at time t + t_0, include all costs
    
'''


'''
Indicators will be functions in the codebase
Parameters will be conditions on their results
May need to make a subclass which contains a indicator+parameter type object
That subclass would allow you to create 'super indicators' which are compositions
of other indicators and parameters.
m
Might look something like

class indicator RSI (RSI, a, b):
    if RSI <= a and RSI >= b:
        
    etc

Then the strategy may look like

class strategy Trend1 (RSI(a,b), Trending(a,b, ...)):
    if conditions met:
        place order

'''

'''
def backtest(strategy, conditions on data tested on):
    over the data given:
        test strategy
        record and compile results
    return results
'''
