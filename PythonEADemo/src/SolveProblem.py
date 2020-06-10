# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:27:35 2020

@author: Andre
"""

import random
import numpy as np

#This program demonstrates key elements of functional evolutionary algorithms
#The program allows for a flexible input int n, and the algorithm is taked with finding, through EA processes
#the target array which is set to a sorted int array of size n


class Parameters:
    #declare editable variables
    n = 10
    maxIterations = 1000
    populationSize = 100
        
    mutationRate = 0.05
    tournamentSize = 10
    crossoverMethod = 2
    
        
class SolveProblem:

    def __init__(self):
        #get variables from the Parameters class and set remaining 
        self.n = Parameters.n
        self.populationSize = Parameters.populationSize
        self.maxIterations = Parameters.maxIterations
        self.mutationRate = Parameters.mutationRate
        self.tournamentSize = Parameters.tournamentSize
        self.crossoverMethod = Parameters.crossoverMethod
        self.fitnessTarget = [0]*self.n
        self.population = np.arange(self.populationSize * self.n).reshape(self.populationSize,self.n)
        for i in range(self.n):
            self.fitnessTarget[i] = i #set target to a sorted int array of size n
        
    def runEA(self):
        self.initialise() #initialise a random population
        counter = bestFitness = 0
        
        for i in range(self.maxIterations):
            child = [0]*self.n #create a new child array of size n
            
            #gather parent genomes from tournament selection
            parentOneIndex = self.tournamentSelect()
            parentTwoIndex = self.tournamentSelect()
            ##create child from parent genetic material, depending on crossove method selected in Parameters
            if self.crossoverMethod == 0: 
                child = self.uniformCrossover(parentOneIndex, parentTwoIndex)
            elif self.crossoverMethod == 1:
                child = self.onepointCrossover(parentOneIndex, parentTwoIndex)
            elif self.crossoverMethod == 2:
                child = self.twopointCrossover(parentOneIndex, parentTwoIndex)
            else: #default case
                child = self.uniformCrossover(parentOneIndex, parentTwoIndex)
            
            #ensure chance to mutate child elements
            child = self.mutate(child)
            childFitness = self.evaluate(child)
            #replace worst parent with child in pop if child is superior 
            self.replaceWorstParent(child, childFitness , parentOneIndex, parentTwoIndex)
            
            bestID, bestFitness = self.findBest()
            
            print("Iteration:" + str(i+1) + " best fitness: " + str(bestFitness) + " member elements: " + str(self.population[bestID]))
            
            if bestFitness == self.n: #solution has been found
                counter = i + 1 
                break
        if bestFitness == self.n:
            print("Solution found on iteration: " + str(counter))
        else:
            print("Solution not found, best fitness: " + str(bestFitness))
    
    def initialise(self):
        for i in range(self.populationSize):
            for x in range(self.n):
                self.population[i][x] = random.randint(0,self.n-1)
    
    def mutate(self, child):
        for i in range(self.n):
            if random.random() < self.mutationRate:
                temp = random.randint(0, self.n-1)
                while temp == child[i]:
                    temp = random.randint(0, self.n-1)
                child[i] = temp
        return child
    
    def tournamentSelect(self):
        tempID = random.randint(0, self.populationSize-1)
        bestID = tempID
        tempFitness = self.evaluate(self.population[tempID])
        bestFitness = tempFitness
        
        for x in range(self.tournamentSize):
            tempID = random.randint(0, self.populationSize-1)
            tempFitness = self.evaluate(self.population[tempID])
            if tempFitness > bestFitness:
                bestFitness = tempFitness
                bestID = tempID
        return bestID
    
    #check crosspoints
    def uniformCrossover(self, parentOneIndex, parentTwoIndex):
        #create new child array
        child = [0]*self.n
        for i in range(self.n):
            if bool(random.getrandbits(1)):
                child[i] = self.population[parentOneIndex][i]
            else:
                child[i] = self.population[parentTwoIndex][i]
        return child
    
    def onepointCrossover(self, parentOneIndex, parentTwoIndex):
        child = [0]*self.n
        crosspoint = random.randint(0, self.n-1)
        for i in range(0, crosspoint):
            child[i] = self.population[parentOneIndex][i]
    
        for j in range(crosspoint, self.n):
            child[j] = self.population[parentTwoIndex][j]
        return child
    
    def twopointCrossover(self, parentOneIndex, parentTwoIndex):
        child=[0]*self.n
        crosspointOne = random.randint(0, self.n-1)
        crosspointTwo = random.randint(0, self.n-1)
        
        if crosspointOne > crosspointTwo:
            temp = crosspointTwo
            crosspointTwo = crosspointOne
            crosspointOne = temp
        
        for i in range(0, crosspointOne):
            child[i] = self.population[parentOneIndex][i]
        
        for j in range(crosspointOne, crosspointTwo):
            child[j] = self.population[parentTwoIndex][j]
            
        for x in range(crosspointTwo, self.n):
            child[x] = self.population[parentOneIndex][x]
    
        return child
    
    
    def evaluate(self, populationMember):
        result = 0
        for i in range(self.n):
            if populationMember[i] == self.fitnessTarget[i]:
                result += 1
        
        return result
    
    def replaceWorstParent(self, child, childFitness, parentOneIndex, parentTwoIndex):
        worstFitness = self.evaluate(self.population[parentOneIndex])
        worstID = parentOneIndex
        tempFitness = self.evaluate(self.population[parentTwoIndex])
        if tempFitness < worstFitness:
            worstFitness = tempFitness
            worstID = parentTwoIndex
        
        if childFitness > worstFitness:
            for i in range(self.n):
                self.population[worstID][i] = child[i]
                
                
            
    def findBest(self):
        #begin with first member of population
        bestFitness = self.evaluate(self.population[0])
        bestID = 0
        
        for i in range(1, self.populationSize):
            tempFitness = self.evaluate(self.population[i])
            if tempFitness > bestFitness:
                bestFitness = tempFitness
                bestID = i
        
        return bestID, bestFitness
    
    
        

