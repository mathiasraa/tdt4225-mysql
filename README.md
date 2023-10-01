_TDT4225 — Large, Distributed Data Volumes_

## Assignment 2 — MySQL Trajectories Database

This assignment looks at an open dataset of trajectories, and the repository contains code that sets up the MySQL database together with different queries. The program is inspired by the social media workout application Strava, where users can track activities like running, walking, biking etc and post them online with stats about their workout.

## Setup

### Prerequisites

- Python
- Docker

### Installation

1. Clone the repository
2. Add the dataset to the `data` folder
3. Run `docker-compose up --build` in the root directory
4. Install the requirements with `pip install -r requirements.txt`
5. Run `migrate.py` to migrate the dataset to the database
