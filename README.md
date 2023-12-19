# ATG-round-2

## Task information:
- Download the CSV file from the link- https://drive.google.com/file/d/1PLYwrGn5YApyWU2QpjbdhM6tea0HuGq7/view?usp=sharing
- Scrape the Twitter profile with Python Selenium or Beautiful Soup
- Details needed are - Bio, Following Count, Followers Count, Location, Website(If available)
- The program should create a CSV file with the above columns.
- The code should be well commented and optimized, there will be extra marks for that
- Make a short video explaining and running the task in <10mins. Don't need to show long-running codes.
- Upload your code to a GitHub public repository
- Submit the video and the GitHub link for the same in the submission form

## Setup
Simply install the required libraries.
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

Bonus: Modularity.  
If you have a valid link of listings, you may also link them.
```
python main.py -l <URL>
```

## Methodology
1. Analysis of required data.
2. Building a basic pipeline for scraping.
3. Testing if the current scraping pipeline works (see [scrape.ipynb](scrape.ipynb)).
4. Application of the pipeline (see [scrape.py](scrape.py)).
5. Deployment.