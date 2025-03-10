# Geographical Data engineering Project


## Description
Project to find the closest point with geographical data, I am not just trying to solve the problem but also aiming to show my coding style. It is also an opportunity for me to receive constructive feedback on what could be improved if a future collaboration is possible.

The pipeline take in entry 3 input:
  - Ref_lat : refrence building latitude
  - Ref_lon : refrence building longitude
  - url : open buildings region file url

When you run the application, it will generate two outputs:

  - The Plus Code of the closest building, shown in the terminal.
  - A plot saved as output.png.

## Requirements
Docker should be running on your environment.

## Installation
Clone the repo Git :
```bash
git clone https://github.com/CharlesDouxPro/Geopgraphic-data-engineering.git
cd Geopgraphic-data-engineering
```

## Run
```bash
docker build -t Geopgraphic-data-container
```
```bash
docker run -v $(pwd):/workspace Geopgraphic-data-container
```

