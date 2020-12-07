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

The goal of our project is to analyze the statistics of cases and deaths caused by COVID-19. 
We selected several states distributed across the United States (Indiana, California, Michigan and, our home state, Ohio) and downloaded the COVID-19 related data published by Health Departments (or equivalent department) of these states.
It turns out that each state stores the data in different format and also have varying data attributes, so converted all datasets into one standardized format which covered the relevant data attributes.
After converting we then pulled the data into our `00 - Project.ipynb` which can receive more states than we did as you just need to add a new script into the `notebook/scripts/` folder for the state and it will auto populate it in the Project notebook.
We wanted things to be replicable across the USA, and you could technically do this worldwide with little tweaking.
In the `00 - Project.ipynb` notebook we have compared different states with each other (all states have some peculiarities) and with data provided by COVID Tracking Project (the state data at the COVID Tracking Project data are closely aligned).
For each of the states we have also compared COVID-19 related deaths with deaths caused by other cause (e.g. heart problems, cancer, stroke, etc).
It turns out that while on the yearly scale COVID-19 does is not as deadly, when looking at it weekly it shoots up to being on the major killers. In Michigan, for example, the peak death weeks from COVID-19 take the 3rd place after heart diseases and cancer.
It is also interesting to note, that during the last weeks the number of deaths caused by unknown and unclassified symptoms is increasing.