# COVID-19 State Comparison & Other Causes of Deaths

## Group Members
 - Aleksey Luchinsky
 - Michael Terry
 - Vagish Vela

## Notebooks Layout
 - notebook/
    - 00 - Project.ipynb : The main project notebook
    - 01 - Ohio.ipynb : Analysis of Ohio
    - 02 - Michigan.ipynb : Analysis of Michigan
    - 03 - Indiana.ipynb : Analysis of Indiana
    - 04 - California.ipynb : Analysis of California
    - 05 - global_daily.ipynb : Analysis of global daily statistics
    - 06 - sex_and_age.ipynb : Analysis of sex and age for death in the USA
    - 07 - report_figures.ipynb : Creation of figures for paper
    - 08 - Ohio_export.ipynb : Export function for ohio (also under scripts/)
    - scripts/ : Contains the preprocessing data for each state to be used in `00 - Project.ipynb`

## Summary

The goal of our project is to analyze the statistics of deaths cases caused by COVID-19 
We selected several states distributed across the United States (Indiana, California, Michigan and, certainly, Ohio) and downloaded the COVID related data published by Health Departments of these states.
It turns out that each state store the data in different format, so converted all datasets into one standardized format.
After such a conversion the comparisons we have compared our results with for different states with each other (all states have some peculiarities) and with data provided by COVID tracker team (good agreement is observed).
For each of the states we have also compared COVID-related deaths with deaths caused by usual reasons (heart problems, cancer, stroke, etc).
It turns out that while on the yearly scale the COVID virus does not look very serious, in the weekly distributions we can easily see its seriousness.
For some states (Michigan, for example) on the peaks COVID takes the 3rd place after heart diseases and cancer.
It is also interesting to note, that during the last weeks the number of deaths caused by some unknown and unclassified symptoms is increasing.