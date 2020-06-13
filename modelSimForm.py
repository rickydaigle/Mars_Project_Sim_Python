#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import HORIZONTAL
from tkinter import END
from tkinter import messagebox
import random
import time

TASK_1_TIME = 1800
TASK_2_TIME = 3600
TASK_3_TIME = 10800
PROD_LOSS_FACTOR = 1.23
PROD_GAIN_FACTOR = 0.8


TASK_1_TIME_DISTRACTED = int(TASK_1_TIME * PROD_LOSS_FACTOR)
TASK_2_TIME_DISTRACTED = int(TASK_2_TIME * PROD_LOSS_FACTOR)
TASK_3_TIME_DISTRACTED = int(TASK_3_TIME  * PROD_LOSS_FACTOR)
TASK_1_TIME_FILTERED = int(TASK_1_TIME * PROD_GAIN_FACTOR)
TASK_2_TIME_FILTERED = int(TASK_2_TIME * PROD_GAIN_FACTOR)
TASK_3_TIME_FILTERED = int(TASK_3_TIME * PROD_GAIN_FACTOR)

TASKS_PER_DAY = 3

fields_dataBaselineLabel = ("Task 1 Baseline (s)", "Task 2 Baseline (s)", "Task 3 Baseline (s)", "Task Repetitions")
fields_dataBaselineEntry = (TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, TASKS_PER_DAY)
fields_dataDistractedLabel = ("Task 1 Distracted (s)", "Task 2 Distracted (s)", "Task 3 Distracted (s)")
fields_dataDistractedEntry = (TASK_1_TIME_DISTRACTED, TASK_2_TIME_DISTRACTED, TASK_3_TIME_DISTRACTED)

teamSize = 0
teamDistracted = 0
distractionAmount = 0.0
difficultyAmount = 0.0
missionDeadline = 0

def getTeamSize():
    teamSize = teamSizeEntry.get()
    return teamSize

def getTeamDistracted():
    teamDistracted = teamDistractedEntry.get()
    return teamDistracted

def getDifficultyAmount():
    difficultyAmount = difficultyAmountEntry.get()
    return difficultyAmount

def getMissionDeadline():
    missionDeadline = missionDeadlineEntry.get()
    return missionDeadline

def getDistractionAmount():
    distractionAmount = distractionAmountEntry.get()
    return distractionAmount

def secs2Days(numSecs):
    numDays = int((((numSecs / 60)/60)/24))
    return numDays

def calcDeadline(TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, teamSize):
    totalTime = ((TASK_1_TIME * int(teamSize)) + (TASK_2_TIME * int(teamSize)) + (TASK_3_TIME * int(teamSize)) * TASKS_PER_DAY)
    deadlineSecs = totalTime + (totalTime * 0.33)
    return deadlineSecs

def getSuggestedDeadline(TASK_1_TIME, TASK_2_TIME, TASK_3_TIME):
    teamSize = getTeamSize()
    try:
        suggestedDeadlineDays = secs2Days(calcDeadline(TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, teamSize))
    except ValueError:
        teamSize = 1
        messagebox.showinfo('Error', 'Team Size must be an integer')
        suggestedDeadlineDays = secs2Days(calcDeadline(TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, teamSize))
    if suggestedDeadlineDays < 1:
        suggestedDeadlineDays = 1
    else:
        suggestedDeadlineDays = suggestedDeadlineDays
    missionDeadlineEntry.delete(0, END)
    missionDeadlineEntry.update()
    missionDeadlineEntry.insert(0, suggestedDeadlineDays)

def getSuggestedDistracted():
    teamSize = int(getTeamSize())
    try:
        suggestedDistracted = round(teamSize * 0.65)
    except ValueError:
        teamSize = 1
        messagebox.showinfo('Error', 'Team Size must be an integer')
        suggestedDistracted = round(teamSize * 0.65)
    if suggestedDistracted < 1:
        suggestedDistracted = 1
    else:
        suggestedDistracted = suggestedDistracted
    teamDistractedEntry.delete(0, END)
    teamDistractedEntry.update()
    teamDistractedEntry.insert(0, suggestedDistracted)
    
window = tk.Tk()
window.title("Human Performance Under Distraction in a Remote Environment - Simulation v1.49")
window.geometry("1200x700")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

dataFrame = tk.Frame(window)
dataFrame.grid(row=0, column=0, sticky="nw")
dataFrame.grid_rowconfigure(0, weight=1)
dataFrame.grid_columnconfigure(0, weight=1)

rowNumber = 0
columnNumber = 0

textrow = tk.Label(dataFrame, text="Task time values calculated from data collection phase: (19% distraction penalty)", anchor="w", font=("bold"))
textrow.grid(row=rowNumber, column=columnNumber, columnspan=6, ipadx=5, pady=1, sticky="w")
rowNumber += 1

x = 0
for field in fields_dataBaselineLabel:
    lbl = tk.Label(dataFrame, text=str(fields_dataBaselineLabel[x]), anchor="w")
    lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
    columnNumber += 1
    lbl = tk.Label(dataFrame, text=str(" " + str(fields_dataBaselineEntry[x]) + "  "), borderwidth=2, relief="sunken")
    lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
    columnNumber += 1
    x += 1

rowNumber += 1
columnNumber = 0

x = 0
for field in fields_dataDistractedLabel:
    lbl = tk.Label(dataFrame, text=str(fields_dataDistractedLabel[x]), width=15, anchor="w")
    lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
    columnNumber  += 1
    lbl = tk.Label(dataFrame, text=str(" " + str(fields_dataDistractedEntry[x]) + "  "), borderwidth=2, relief="sunken")
    lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
    columnNumber  +=1
    x += 1

rowNumber += 1
columnNumber = 0

blankrow = tk.Label(dataFrame, text=" ", anchor="w")
blankrow.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=1, sticky="w")
rowNumber += 1

textrow = tk.Label(dataFrame, text="Enter test variables below:", anchor="w", font=("bold"))
textrow.grid(row=rowNumber, column=columnNumber, columnspan=6, ipadx=5, pady=1, sticky="w")
rowNumber += 1

startRow = rowNumber

lbl = tk.Label(dataFrame, text="Total Team Size:", anchor="w")
lbl.grid(row=rowNumber, column=columnNumber, columnspan=2, ipadx=3, pady=3, sticky="w")
rowNumber += 1
lbl = tk.Label(dataFrame, text="Distracted Members: (~65% of total)", anchor="w")
lbl.grid(row=rowNumber, column=columnNumber, columnspan=2, ipadx=3, pady=3, sticky="w")
rowNumber += 1
lbl = tk.Label(dataFrame, text="Mission Deadline (# Days):", anchor="w")
lbl.grid(row=rowNumber, column=columnNumber, columnspan=2, ipadx=3, pady=3, sticky="w")

rowNumber = startRow
columnNumber += 2

teamSizeEntry = tk.Entry(dataFrame)
teamSizeEntry.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
rowNumber += 1
teamDistractedEntry = tk.Entry(dataFrame)
teamDistractedEntry.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
suggestButt = tk.Button(dataFrame, text="Get Suggested Distracted #", command=lambda : getSuggestedDistracted())
suggestButt.grid(row=rowNumber, column=columnNumber+1, columnspan=2, ipadx=5, pady=3, sticky="w")
rowNumber += 1
missionDeadlineEntry = tk.Entry(dataFrame)
missionDeadlineEntry.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
suggestBut = tk.Button(dataFrame, text="Get Suggested Deadline", command=lambda : getSuggestedDeadline(TASK_1_TIME, TASK_2_TIME, TASK_3_TIME))
suggestBut.grid(row=rowNumber, column=columnNumber+1, columnspan=2, ipadx=5, pady=3, sticky="w")

rowNumber += 1
columnNumber = 0

blankrow = tk.Label(dataFrame, text=" ", anchor="w")
blankrow.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=1, sticky="w")

rowNumber += 1

lbl = tk.Label(dataFrame, text="Distraction Level - Default is 100% distracted. Less than 100% reduces distraction level. (FILTER ON = -1%)", anchor="w")
lbl.grid(row=rowNumber, columnspan=6, ipadx=5, pady=3, sticky="w")
rowNumber += 1
distractionAmountEntry = tk.Scale(dataFrame, from_=-1, to_=100, orient=HORIZONTAL, length=450, tickinterval=25)
distractionAmountEntry.set(100)
distractionAmountEntry.grid(row=rowNumber, column=columnNumber, columnspan=6, padx=5, pady=3, sticky="w")
rowNumber += 1

blankrow = tk.Label(dataFrame, text=" ", anchor="w")
blankrow.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=1, sticky="w")
rowNumber += 1

lbl = tk.Label(dataFrame, text="Task Difficulty - Default is 100%. More than 100% makes tasks harder, less makes them easier.", anchor="w")
lbl.grid(row=rowNumber, column=columnNumber, columnspan=6, ipadx=5, pady=3, sticky="w")
rowNumber += 1
difficultyAmountEntry = tk.Scale(dataFrame, from_=0, to_=200, orient=HORIZONTAL, length=450, tickinterval=50)
difficultyAmountEntry.set(100)
difficultyAmountEntry.grid(row=rowNumber, column=columnNumber, columnspan=6, padx=5, pady=3, sticky="w")
rowNumber += 1

def runSimulation(rowNumber, columnNumber, TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, TASK_1_TIME_DISTRACTED, TASK_2_TIME_DISTRACTED, TASK_3_TIME_DISTRACTED, TASKS_PER_DAY, TASK_1_TIME_FILTERED, TASK_2_TIME_FILTERED, TASK_3_TIME_FILTERED):
    teamSize = int(getTeamSize())
    teamDistracted = int(getTeamDistracted())
    missionDeadline = int(getMissionDeadline())
    teamFocused = teamSize - teamDistracted
    difficultyAmount = float(getDifficultyAmount()/100)
    distractionAmount = float(getDistractionAmount()/100)

    if distractionAmount >= 0:
    
        task1_Baseline = (TASK_1_TIME * teamSize) * TASKS_PER_DAY
        task1_DifficultyOnly = (((TASK_1_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task1_Baseline
        task1_DistractionOnly = ((((TASK_1_TIME_DISTRACTED - TASK_1_TIME) * distractionAmount) * teamDistracted) * TASKS_PER_DAY)
        if task1_DistractionOnly < 0:
            task1_DistractionOnly = 0.00000
            task1_Actual = (((TASK_1_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task1_Actual = (((TASK_1_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + ((task1_DistractionOnly * difficultyAmount) + (TASK_1_TIME * teamDistracted) * TASKS_PER_DAY)
        
        task2_Baseline = (TASK_2_TIME * teamSize) * TASKS_PER_DAY
        task2_DifficultyOnly = (((TASK_2_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task2_Baseline
        task2_DistractionOnly = ((((TASK_2_TIME_DISTRACTED - TASK_2_TIME) * distractionAmount) * teamDistracted) * TASKS_PER_DAY)
        if task2_DistractionOnly < 0:
            task2_DistractionOnly = 0.00000
            task2_Actual = (((TASK_2_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task2_Actual = (((TASK_2_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + ((task2_DistractionOnly * difficultyAmount) + (TASK_2_TIME * teamDistracted) * TASKS_PER_DAY)
        
        task3_Baseline = (TASK_3_TIME * teamSize)* TASKS_PER_DAY
        task3_DifficultyOnly = (((TASK_3_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task3_Baseline
        task3_DistractionOnly = ((((TASK_3_TIME_DISTRACTED - TASK_3_TIME) * distractionAmount) * teamDistracted) * TASKS_PER_DAY)
        if task3_DistractionOnly < 0:
            task3_DistractionOnly = 0.00000
            task3_Actual = (((TASK_3_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task3_Actual = (((TASK_3_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + ((task3_DistractionOnly * difficultyAmount) + (TASK_3_TIME * teamDistracted) * TASKS_PER_DAY)
        
        taskAll_Baseline = task1_Baseline + task2_Baseline + task3_Baseline
        taskAll_DifficultyOnly = task1_DifficultyOnly + task2_DifficultyOnly + task3_DifficultyOnly
        taskAll_DistractionOnly = task1_DistractionOnly + task2_DistractionOnly + task3_DistractionOnly
        taskAll_Actual = task1_Actual + task2_Actual + task3_Actual
        taskAll_Days = secs2Days(taskAll_Actual)
        if taskAll_Days > missionDeadline:
            missionStatus = "FAILED"
        else:
            missionStatus = "SUCCESS"

        fields_simulationLabel_1 = ("Task 1 Baseline", "Difficulty Only", "Distraction Only", "Task 1 Actual")
        fields_simulationEntry_1 = (task1_Baseline, task1_DifficultyOnly, task1_DistractionOnly, task1_Actual)
        fields_simulationLabel_2 = ("Task 2 Baseline", "Difficulty Only", "Distraction Only", "Task 2 Actual")
        fields_simulationEntry_2 = (task2_Baseline, task2_DifficultyOnly, task2_DistractionOnly, task2_Actual)
        fields_simulationLabel_3 = ("Task 3 Baseline", "Difficulty Only", "Distraction Only", "Task 3 Actual")
        fields_simulationEntry_3 = (task3_Baseline, task3_DifficultyOnly, task3_DistractionOnly, task3_Actual)
        fields_simulationLabel_final = ("Mission Baseline", "Difficulty Only", "Distraction Only", "Mission Actual", "Mission Days", "Mission Deadline", "Mission Status")
        fields_simulationEntry_final = (taskAll_Baseline, taskAll_DifficultyOnly, taskAll_DistractionOnly, taskAll_Actual, taskAll_Days, missionDeadline, missionStatus)

        blankrow = tk.Label(dataFrame, text=" ", anchor="w")
        blankrow.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=1, sticky="w")
        rowNumber += 1
        textrow = tk.Label(dataFrame, text="Simulated Mission Statistics:", anchor="w", font=("bold"))
        textrow.grid(row=rowNumber, column=columnNumber, columnspan=6, ipadx=5, pady=1, sticky="w")
        rowNumber += 1

        x = 0
        for field in fields_simulationLabel_1:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_1[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_1[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_2:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_2[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_2[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_3:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_3[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_3[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_final:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_final[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_final[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

    else:

        task1_Baseline = (TASK_1_TIME * teamSize) * TASKS_PER_DAY
        task1_DifficultyOnly = (((TASK_1_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task1_Baseline
        task1_DistractionOnly = 0
        if task1_DistractionOnly < 0:
            task1_DistractionOnly = 0.00000
            task1_Actual = (((TASK_1_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task1_Actual = (((TASK_1_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + (((TASK_1_TIME_FILTERED * difficultyAmount) * teamDistracted) * TASKS_PER_DAY)
        
        task2_Baseline = (TASK_2_TIME * teamSize) * TASKS_PER_DAY
        task2_DifficultyOnly = (((TASK_2_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task2_Baseline
        task2_DistractionOnly = 0
        if task2_DistractionOnly < 0:
            task2_DistractionOnly = 0.00000
            task2_Actual = (((TASK_2_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task2_Actual = (((TASK_2_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + (((TASK_2_TIME_FILTERED * difficultyAmount) * teamDistracted) * TASKS_PER_DAY)
        
        task3_Baseline = (TASK_3_TIME * teamSize)* TASKS_PER_DAY
        task3_DifficultyOnly = (((TASK_3_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY) - task3_Baseline
        task3_DistractionOnly = 0
        if task3_DistractionOnly < 0:
            task3_DistractionOnly = 0.00000
            task3_Actual = (((TASK_3_TIME * difficultyAmount) * teamSize) * TASKS_PER_DAY)
        else:
            task3_Actual = (((TASK_3_TIME * difficultyAmount) * teamFocused) * TASKS_PER_DAY) + (((TASK_3_TIME_FILTERED * difficultyAmount) * teamDistracted) * TASKS_PER_DAY)
        
        taskAll_Baseline = task1_Baseline + task2_Baseline + task3_Baseline
        taskAll_DifficultyOnly = task1_DifficultyOnly + task2_DifficultyOnly + task3_DifficultyOnly
        taskAll_DistractionOnly = task1_DistractionOnly + task2_DistractionOnly + task3_DistractionOnly
        taskAll_Actual = task1_Actual + task2_Actual + task3_Actual
        taskAll_Days = secs2Days(taskAll_Actual)
        if taskAll_Days > missionDeadline:
            missionStatus = "FAILED"
        else:
            missionStatus = "SUCCESS"

        fields_simulationLabel_1 = ("Task 1 Baseline", "Difficulty Only", "Distraction Only", "Task 1 Actual")
        fields_simulationEntry_1 = (task1_Baseline, task1_DifficultyOnly, task1_DistractionOnly, task1_Actual)
        fields_simulationLabel_2 = ("Task 2 Baseline", "Difficulty Only", "Distraction Only", "Task 2 Actual")
        fields_simulationEntry_2 = (task2_Baseline, task2_DifficultyOnly, task2_DistractionOnly, task2_Actual)
        fields_simulationLabel_3 = ("Task 3 Baseline", "Difficulty Only", "Distraction Only", "Task 3 Actual")
        fields_simulationEntry_3 = (task3_Baseline, task3_DifficultyOnly, task3_DistractionOnly, task3_Actual)
        fields_simulationLabel_final = ("Mission Baseline", "Difficulty Only", "Distraction Only", "Mission Actual", "Mission Days", "Mission Deadline", "Mission Status")
        fields_simulationEntry_final = (taskAll_Baseline, taskAll_DifficultyOnly, taskAll_DistractionOnly, taskAll_Actual, taskAll_Days, missionDeadline, missionStatus)

        blankrow = tk.Label(dataFrame, text=" ", anchor="w")
        blankrow.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=1, sticky="w")
        rowNumber += 1
        textrow = tk.Label(dataFrame, text="Simulated Mission Statistics:", anchor="w", font=("bold"))
        textrow.grid(row=rowNumber, column=columnNumber, columnspan=6, ipadx=5, pady=1, sticky="w")
        rowNumber += 1

        x = 0
        for field in fields_simulationLabel_1:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_1[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_1[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_2:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_2[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_2[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_3:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_3[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_3[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1

        rowNumber += 1
        columnNumber = 0

        x = 0
        for field in fields_simulationLabel_final:
            lbl = tk.Label(dataFrame, text=str(fields_simulationLabel_final[x]), anchor="w")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            lbl = tk.Label(dataFrame, text=str(" " + str(fields_simulationEntry_final[x]) + "  "), borderwidth=2, relief="sunken")
            lbl.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3, sticky="w")
            columnNumber += 1
            x += 1
    
submitBut = tk.Button(window, text="Run Simulation", command=lambda : runSimulation(rowNumber, columnNumber, TASK_1_TIME, TASK_2_TIME, TASK_3_TIME, TASK_1_TIME_DISTRACTED, TASK_2_TIME_DISTRACTED, TASK_3_TIME_DISTRACTED, TASKS_PER_DAY, TASK_1_TIME_FILTERED, TASK_2_TIME_FILTERED, TASK_3_TIME_FILTERED))
submitBut.grid(row=rowNumber, column=columnNumber, ipadx=5, pady=3)

window.mainloop()
