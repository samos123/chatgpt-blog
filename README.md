# chatgpt-blog: Flask, Stackoverflow API and chatGPT
A prototype to implement a blog that relies on Stackoverflow to get questions
and uses chatGPT to provide an answer. This was purely done for educational purposes to
see whether chatGPT is effective and correct.

Live demo: [https://golangqna.com](https://golangqna.com)

## Loading new data
First load data from StackOverflow e.g. from Jan 4 to Jan 5:
```
python models.py load_so_data 2023-01-04 2023-01-05
```

Afterwards run generate answers script that uses chat GPT:
```
python models.py generate_answers
```
