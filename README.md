# Overview

To define and calculate a bike score for a particular bike ride similar to a walk or transit score. 

# How is it calculated?

## Factors to consider:

<ul>
  <li>Elevation gain over specified distance</li>
  <li>Bike path availability, bike path > bike lane in road > no bike lane</li>
  <li>When riding on a road, what is the condition of the road? Residential? Speed?</li>
  <li>Incidents along route, as some indication of safety</li>
</ul>

# Project Status

This project is in early development phase. 

Current status: bike_score is only based on elevation of route

# Thought process

My goal is to create an API endpoint which can be passed content and from that calculate a bike score. The bike score by evaluating information collected via series of API calls, nothing is stored. There is also no visual display for any of this content. For this reason, I thought that Flask, a lightweight framework would be the best way to build this. Although Django does do a lot of useful things, in this scenario, I wouldn't have used 99% of them.

This is the first Flask app that I have built so will likely have a bit of iteration.

# How to run
```
export FLASK_APP=bike_score.py
flask run
```

# How to run tests
Test run using pytest and coverage. Install these, if you haven't already (`pip3 install pytest coverage`)

Install app locally -> `pip3 install -e .`

Run tests -> `pytest`