# Trail Trekker Data Pipeline

A data pipeline project built for the [Learn Analytics Engineering Data Pipeline Summer](https://learnanalyticsengineering.substack.com/t/data-pipeline-summer) challenge.

## Problem

As someone new to analytics engineering, I needed hands-on experience with modern data stack tools and best practices. While I've started using dbt at work, I wanted to understand tools like SQLMesh and different approaches to data modeling and pipeline orchestration. The challenge was to build a complete data pipeline from raw data ingestion to analysis-ready models while learning these concepts from scratch. Madison provides a lot of helpful tips along the way.

## About the Data

This project uses a fictional trail hiking dataset that includes:
- Customer data: User profiles, demographics, and hiking preferences
- Subscription data: Plan info, pricing tiers, and feature sets
- Plan features: Breakdown of what each subscription tier offers
- Subscription changes: Historical tracking of customer plan modifications

The data reads like a trail hiking app business model with multiple subscription tiers and customer lifecycle tracking.

## Approach

**Data Ingestion:**
- DuckDB - Local analytics database for development and testing. First time using this! Chose this one for being lightweight, easy to implement, and the datasets are all well within the RAM range free on this laptop.

**Data Modeling:**
- SQLMesh - Data transformation and modeling framework (alternative to dbt) Also my first time using this! I've used dbt at work to have a place to plan and show where all these metrics come from (lineage!), but was excited for some exposure to other options.
- Architecture: Went with medallion architecture because the relative level of changes needed. Wanted to keep the existing dataset as-is in case we need more from it later, but wanted to bring it together so it's more analytics ready. 
- Business Problem to solve for:
  - A new customer/subscription is NOT considered a subscription change but a cancellation is
  - A customer will always retain their subscription_id, unless they cancel and then start a new subscription
  - When a customer switches plans, the end date of the first subscription plan is the start date of the next subscription plan
  - A customer can't change their plan more than once per day
Ended up making fct_subscription_changes to account for these requests. 
-Orchestration: To mimic a similar refresh schedule to something in use at work, I created a cron job that refreshes these on an hourly basis. Being duckdb was picked for being lightweight and able to run on my bag of potatoes, it only makes sense to keep it simple and run it as a cron job. Sure, we could move to like an Airflow, but that would be overengineered for this scope. If we would move this to a production environment, or a VM or always-on PC we could look at orchestration using something like that instead.


**Methodology:**
- Implemented a medallion architecture with raw → staging → mart layers
- Built in some automated data quality checks and audits
- Created fact table to track subscription changes over time
- Used two different environments, dev and prod, to test then push changes into.

## Decisions and Roadblocks

**Key Decisions:**
- Using SQLMesh: This one is completely new to me as of this project. I have used dbt cloud, done some jinja, and deployed under 100 models in production. I found dbt and dbt cloud very easy to pick up, so I was hoping SQLMesh was similar (based on all the ads I keep seeing)
- Used DuckDB: Also first time using this and _pleasantly_ surprised with its snappiness and simplicity. 
- Implemented data type casting and null handling in staging models: To keep things rolling with less models, I put some of the casting in the stage models. Didn't want to edit the raw data in case we needed something from it later on!

**Roadblocks Encountered:**
- Learning curve with SQLMesh syntax and concepts: There's some similarities but definite differences from dbt. Doing a fetchdf felt weird, but worked fine.
- Learning curve with duckdb: I know it's not supposed to be a problem, but man, I kept forgetting to open/attach the database when I picked up the project again after a stop. 
- Setting up proper automated scheduling and monitoring for the pipeline, but on a macOS: I'm a windows guy from my early days hacking together pieces of leftover PC, overclocking the sparks out of a gfx card, and using Windows my whole professional career, so trying this out on a mac was new all around being a longtime Windows user. Setting up a cron .sh file and using vim was a weird one. Had to make a temp file, save it, add in the schedule, then it would work. 

## Solution and/or Next Steps

**Current Status:** Core pipeline is functional with automated cron scheduling

**Completed:**
- Raw data ingestion and staging transformations
- Fact table for subscription change tracking
- Automated pipeline execution via cron job
- Data quality audits and testing in models

## Project Structure

```
Data_Pipeline_Summer_2025/
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
├── cron_job.sh                 # Automated pipeline execution script
├── trail_trekker.db            # DuckDB database file
├── *.csv                       # Raw data files (customers, features, plans, etc.)
├── advanced_subscription_analysis.py  # Subscription metrics visualization script
├── advanced_subscription_analysis.png # Generated analysis chart
└── trail-trekker/             # SQLMesh project
    ├── config.yaml            # SQLMesh configuration
    ├── models/                # SQL transformation models
    │   ├── *_raw.sql         # Raw data models
    │   ├── staging_*.sql     # Staging layer models
    │   ├── dim_*.sql         # Dimension models
    │   └── fct_*.sql         # Fact table models
    ├── audits/               # Data quality checks
    ├── tests/                # Model tests
    ├── seeds/                # Reference data
    └── macros/               # Reusable SQL functions
```

**Follow-up Analysis:**
As a demonstration of AI's effectiveness for summary and analysis tasks, used Claude Code to generate a quick visualization script (`advanced_subscription_analysis.py`) that shows key subscription ratios and metrics to help explain the current subscription makeup of the business.

## Who am I?

I'm a data professional diving headfirst into analytics engineering. Started as a data analyst and now I get to head up strategerie(Bush-ism) , at a financial institution. Having recently started using dbt at work, I wanted to get more experience with data modeling and how different tools approach architecture. I'm learning everything here from scratch, with the exception of database concepts, data vizualization, and SQL usage. Give me a shout, good or bad, at https://www.linkedin.com/in/israel-spence/
