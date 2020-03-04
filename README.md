# Overview

To define and calculate a bike score for a particular bike ride similar to a walk or transit score.

## What is it and how is it calculated?

A bike score is a way to assess a bike route. Scores are out of 100. This API endpoint also provides scores for elevation grade, safety, and bike lane availability. These scores are also out of 100.

### Factors to consider:

<ul>
  <li>Elevation gain over specified distance</li>
  <li>Bike path availability, bike path > bike lane in road > no bike lane</li>
  <li>Incidents along route, as some indication of safety</li>
</ul>

### How is the score calculated?

The score will be be out of 100 with each factor making up an equal percentage of the score.

#### Inputs
<ul>
  <li>`total_distance` - total distance of route, in miles</li>
  <li>`points_of_elevation` - an even sampling of elevation throughout the ride, in feet</li>
  <li>`bike_lane_availability` - percentage of bike ride on a bike path</li>
  <li>`safety_incidents` - number of safety incidents that have occurred in the path 90 days along route</li>
</ul>

## Project Status

This project is in early development phase.

The ultimate goal is to pass in a start and end point and calculate the score based on this. Based on my initial research, I think I can do most of this through the Google Maps API. I will need to leverage state road data to get the safety incidents. I suspect understanding how many happened along a particular route being a big challenge because I will have to map incidents to points and then determine if a route goes through or near that point.

Right now, API integration is not complete, therefore, users must submit each factor (elevation gain, bike path availability, etc.) through the API.

## Thought process

This is the first Flask app that I have built so will likely have a bit of iteration.

I chose to use Flask because I wanted to create an API endpoint for an app that had no front end and no DB.  For this reason, I thought that Flask, a lightweight framework would be the best way to build this.

## How to run
```
export FLASK_APP=bike_score_app
export FLASK_ENV=development
flask run
```

### Activate virtual environment to develop locally
```
source venv/bin/activate
```

### Sample request

Note, this sample request assumes you are running this on your host machine.

```
curl -X POST \
  http://127.0.0.1:5000/api/bike_score?
    total_distance=6.9&
    points_of_elevation=[1, 3.2, 5.0, 9.9, 1]&
    bike_lane_availability=40&
    safety_incidents=2
```

### Sample response

```
{
  "data": {
    "bike_grade_score": 99.3551,
    "bike_lane_availability_score": 40,
    "bike_safety_score": 33.3333,
    "bike_score": 58
  }
}
```

## How to run tests
Test run using pytest and coverage. Install these, if you haven't already (`pip3 install pytest coverage`)

Install app locally -> `pip3 install -e .`

Run tests -> `pytest`
