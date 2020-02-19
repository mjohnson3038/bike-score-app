# Overview

To define and calculate a bike score for a particular bike ride similar to a walk or transit score.

## How is it calculated?

### Factors to consider:

<ul>
  <li>NOT IMPLEMENTED - Elevation gain over specified distance</li>
  <li>NOT IMPLEMENTED - Bike path availability, bike path > bike lane in road > no bike lane</li>
  <li>NOT IMPLEMENTED - When riding on a road, what is the condition of the road? Residential? Speed?</li>
  <li>NOT IMPLEMENTED - Incidents along route, as some indication of safety</li>
</ul>

### How is the score calculated?

The score will be be out of 100 with each factor making up an equal percentage of the score.

## Project Status

This project is in early development phase.

The ultimate goal is to pass in a route and calculate the score based on this.

Right now, API integration is not complete, therefore, users must submit each factor (elevation gain, bike path availability, etc.) through the API. I may eventually add documentation but that can be accomodated through Flask.

## Thought process

This is the first Flask app that I have built so will likely have a bit of iteration.

I chose to use Flask because I wanted to create an API endpoint for an app that had no front end and no DB.  For this reason, I thought that Flask, a lightweight framework would be the best way to build this.

## How to run
```
export FLASK_APP=bike_score_app
export FLASK_ENV=development
flask run
```

### Sample request

Note, this sample request assumes you are running this on your host machine.

```
curl -X POST \
  localhost:5000/api/bike_score \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
      "bike_lane_availability_score": 40,
      "bike_score": 79
    }
  }'
```

## How to run tests
Test run using pytest and coverage. Install these, if you haven't already (`pip3 install pytest coverage`)

Install app locally -> `pip3 install -e .`

Run tests -> `pytest`
