# MovieSphere

**Movie Recommendation and Viewing Pattern Analysis Using Big Data**

MovieSphere is a movie analytics and recommendation platform built
around the MovieLens dataset. It combines a web dashboard with a
data-processing pipeline and collaborative-filtering recommendations
using Spark MLlib ALS.

## Overview

MovieSphere is designed to process movie ratings and provide:

-   Movie discovery and title search
-   Analytics such as rating distributions, genre breakdowns, and
    activity patterns
-   Personalized recommendations generated with collaborative filtering
-   Movie-to-movie recommendations and user insights
-   A web interface backed by a Flask API

The application follows a **batch-processing and artifact-serving**
approach: analytics and recommendation jobs run separately and save
results as artifacts. The Flask application can then serve those
prepared results without starting Spark for every web request.

## Technology Stack

  Layer             Technologies
  ----------------- -----------------------------------------------
  Frontend          HTML, CSS, JavaScript, Chart.js, Font Awesome
  Web application   Flask, Jinja2
  Data processing   Pandas, NumPy, Spark SQL
  Big Data / ML     PySpark, Spark MLlib ALS
  Deployment        Render, Gunicorn
  Dataset           MovieLens Latest Small

## Project Structure

``` text
MovieSphere/
├── app.py
├── requirements.txt
├── Procfile
├── data/
│   ├── ml-latest-small/
│   ├── processed/
│   └── models/
│       └── als_output/
├── data_layer/
│   ├── loader.py
│   ├── service.py
│   └── artifacts.py
├── spark_jobs/
│   ├── common.py
│   ├── spark_analytics.py
│   └── als_model.py
├── static/
│   ├── css/
│   └── js/
├── templates/
└── scripts/
    ├── run_pipeline.sh
    └── verify_als.py
```

Folder contents may vary slightly as the project evolves. The
`data/ml-latest-small/readme.txt` file belongs to the MovieLens dataset;
it is separate from this project README.

## Getting Started

### Requirements

-   Python 3.10 or a compatible version supported by the project's
    dependencies
-   Java 11 or 17 for running PySpark locally
-   MovieLens Latest Small dataset

If Java is not available, use the Pandas engine where supported by the
pipeline.

### 1. Clone the repository

``` bash
git clone https://github.com/Akshaya-k97/MovieSphereProject.git
cd MovieSphereProject
```

### 2. Install Python dependencies

``` bash
pip install -r requirements.txt
```

### 3. Place the dataset

Download the [MovieLens Latest Small
dataset](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)
and extract it into:

``` text
data/ml-latest-small/
```

Ensure that `movies.csv` and `ratings.csv` are present in that folder.
Keep MovieLens' own `readme.txt` with the dataset if desired.

### 4. Generate analytics and recommendation artifacts

Run the processing jobs once to generate the data consumed by the
application.

**Using Spark (requires Java):**

``` bash
python -m spark_jobs.spark_analytics
python -m spark_jobs.als_model
```

**Using the Pandas fallback (if supported by your local project
version):**

``` bash
python -m spark_jobs.spark_analytics --engine pandas
python -m spark_jobs.als_model --engine pandas
```

The jobs are expected to create analytics and recommendation outputs
under `data/processed/` and `data/models/als_output/`. Exact output
files depend on the pipeline configuration.

### 5. Verify recommendation artifacts

If the repository includes the validation script, run:

``` bash
python scripts/verify_als.py
```

Review its output before enabling ALS recommendations.

### 6. Start the Flask application

Set the environment variable to enable the ALS recommendation path, if
the generated artifacts are ready.

**Windows PowerShell:**

``` powershell
$env:MOVIESPHERE_USE_ALS = "1"
python app.py
```

**Linux / macOS:**

``` bash
export MOVIESPHERE_USE_ALS=1
python app.py
```

Then open <http://127.0.0.1:5000/> in your browser.

If ALS is not enabled or its artifacts are unavailable, the application
may use its configured fallback recommendation behavior.

## Configuration

  -----------------------------------------------------------------------
  Environment variable                Purpose
  ----------------------------------- -----------------------------------
  `MOVIESPHERE_USE_ALS`               Enables the ALS-based
                                      recommendation path when set to `1`

  `MOVIELENS_DIR`                     Optional custom path to the
                                      MovieLens dataset

  `SPARK_MASTER`                      Optional Spark master setting;
                                      commonly `local[*]` for local
                                      execution
  -----------------------------------------------------------------------

Set environment variables in your local shell or deployment environment.
Do not hardcode secrets in source files.

## API Overview

The Flask backend exposes API routes for movie data, analytics, user
insights, and recommendations. The routes implemented in the current
project include:

  ----------------------------------------------------------------------------------
  Method                  Endpoint                           Description
  ----------------------- ---------------------------------- -----------------------
  GET                     `/api/movies`                      Returns movie data

  GET                     `/api/movies/search?q=`            Searches movie titles

  GET                     `/api/movies/<id>`                 Returns details for one
                                                             movie

  GET                     `/api/analytics`                   Returns dashboard
                                                             analytics

  GET                     `/api/user/<id>/insights`          Returns insights for a
                                                             user

  GET                     `/api/user/<id>/recommendations`   Returns personalized
                                                             recommendations when
                                                             available

  GET                     `/api/recommendations/<id>`        Returns recommendations
                                                             related to a movie

  GET                     `/api/artifacts/status`            Reports recommendation
                                                             artifact and feature
                                                             status
  ----------------------------------------------------------------------------------

API availability and response fields can depend on the current
application configuration and whether generated artifacts are present.
Refer to the route definitions in `app.py` for the exact response
schema.

## Recommendation Model

MovieSphere uses **Alternating Least Squares (ALS)**, a
collaborative-filtering method available in Spark MLlib. ALS learns
latent representations of users and movies from rating interactions and
uses them to estimate relevant recommendations.

The project's documented training configuration is:

  Parameter                  Value
  -------------------------- ---------
  Rank                       50
  Maximum iterations         10
  Regularization parameter   0.1
  Cold-start strategy        `drop`
  Non-negative factors       Enabled
  Random seed                42

The model is trained offline, and recommendation results are saved for
application use. A displayed match percentage, where present, should be
understood as a relative UI score rather than a calibrated probability
that a user will like a movie.

## Big Data and Cloud Computing Context

The project demonstrates a data pipeline that separates batch
computation from web serving:

1.  Load the MovieLens ratings and movie metadata.
2.  Process and aggregate the data using the configured processing
    engine.
3.  Train the ALS recommendation model.
4.  Save analytics and recommendation outputs as artifacts.
5.  Serve those artifacts through the Flask API and dashboard.

The architecture is suitable for demonstrating local batch processing
and can be extended to cloud-based storage and distributed execution.
Cloud services such as object storage or managed Spark infrastructure
are future integration options unless they are explicitly configured in
the deployed version.

## Limitations and Future Enhancements

-   Evaluate recommendation quality with metrics such as Precision@K,
    Recall@K, and NDCG.
-   Explore hybrid recommendations combining collaborative filtering
    with movie metadata.
-   Improve recommendations for new users and movies with limited rating
    history.
-   Integrate cloud object storage for datasets and generated artifacts.
-   Explore managed distributed Spark execution for larger datasets.
-   Consider streaming updates if real-time ingestion becomes a project
    requirement.

## Dataset and Citation

This project uses the MovieLens dataset provided by GroupLens Research.
Please retain and follow the dataset's included terms and citation
guidance.

Harper, F. Maxwell, and Joseph A. Konstan. 2015. "The MovieLens
Datasets: History and Context." *ACM Transactions on Interactive
Intelligent Systems*.

Dataset: [MovieLens Latest
Small](https://grouplens.org/datasets/movielens/)

## License

This is an academic project. No separate license is specified here;
check the repository for any license file and the MovieLens dataset
terms before reuse or redistribution.
