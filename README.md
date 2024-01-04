# ATG-round-3

## Task information:
- It will be a continuation of your Second task.
- Refer to the second shortlisting task, instead of CSV store those scraped data in a MySQL or PostgreSQL Database.
- Here is a video of how to use MySQL with Python:  https://www.youtube.com/watch?v=3vsC05rxZ8c
- Make a short video explaining and running the task in <10mins. Don't need to show long-running codes.
- Upload your code to a GitHub public repository
- Submit the video and the GitHub link for the same in the submission form

## Setup
1. Set up a user and stuff.
2. Simply install the required libraries.  
```bash
pip install -r requirements.txt
```  
Maintaining a virtual environment is recommended.

## Running The Code
To run the code simply run the following.
```bash
python main.py
```
Once the output is ready, it will be stored in `out/`.

**Note**: You can also run the code step by stem in the python notebook at [steps.ipynb](steps.ipynb)


**Bonus**: Multiprocessing.  
Scraping runs on multiple processes. This creates a much more scalable result.

## Methodology
1. Analysis of required data.
2. Building a basic pipeline for scraping.
3. Testing if the current scraping pipeline works (see [test.ipynb](test.ipynb)).
4. Application of the pipeline (see [scraper.py](scraper.py)).
5. Deployment.