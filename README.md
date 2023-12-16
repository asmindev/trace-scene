# KD Trace

Find the korean drama just with screenshot

## Authors

-   Code fork from [nafis](https://www.github.com/salismazaya/nafis) by [@salismazaya](https://www.github.com/salismazaya)
-   [@asmindev](https://www.github.com/asmindev)

## How does this work?

The video is split into frames (in my case, I split 2 frames/second), then the frames are saved as a vector/matrix and the default model used is the resnet-18.

## Run Locally

Clone the project and highly recommended to make a virtual enviroment

```bash
  git clone https://github.com/asmindev/trace-scene
```

Go to the project directory

```bash
  cd trace-scene
```

Install dependencies

```bash
  pip install -r requirements
```

Adding video to database follow this [instruction](https://www.github.com/asmindev/trace-scene#add-series)

Start the server

```bash
  python3 app.py
```

Testing

```bash
  curl -X POST -F "file=@path/to/your/file.jpg" http://localhost:5000/search

```

## Add Series

Folder videos structure

```md
videos
│ ├── Series-name-1
│ │ ├── 001.mp4 # eps 1
│ │ └── 002.mp4 # eps 2
│ │
│ ├── Series-name-2
│ │ ├── 001.mp4
│ │ ├── 002.mp4
│ │ └── 002.mp4
│ │
│ ├── Series-name-3
│ │ ├── 001.mp4
│ │ └── 002.mp4
│ │
│ └── Series-name-4
│ ├── 001.mp4
│ ├── 002.mp4
│ └── 002.mp4
│
├── bulk_split_video.py
├── add_to_database.py
└── app.py
```

Splitting video and save to pickle

```bash
python3 bulk_split_video.py

```

Add pickle to vector database

```bash
python3 add_to_database.py

```

## Tech Stack

**Server:** Flask

**Database:** Chromadb

**Machine Learning:** pytorch, img2vec
