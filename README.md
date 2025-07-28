# Adobe Hackathon Round 1A – Heading Extractor

## Overview

This script extracts a hierarchical outline (Title, H1, H2, H3) from any PDF using font size analysis via PyMuPDF.

## 🔧 Run Instructions

# Step 1: Build Docker image

```
docker build --platform linux/amd64 -t heading-extractor:latest .
```

# Step 2: Run solution

```
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none heading-extractor:latest
```
