# OCR-based ID Scraper

This repository contains a prototype for an OCR-based ID Scraper using Streamlit and Tesseract. The prototype demonstrates the extraction of key data points from an example ID image and presents them in a structured format that is editable, and then can be downloaded in several common file format types.

[check out the first demo here](https//:idextract.streamlit.app)

and [the second demo here](https//:idextract2.streamlit.app)

## Concept
The core idea is to allow users to extract specific information fields from ID images (like driver's licenses). The current implementation focuses on demonstrating the concept with a predefined example image provided by the Department of Homeland Security.

## Two Approaches

There are two `.py` files in this repository. `pytesseract.py` illustrates a basic approach that is meant to service a client whom wants to `custom train` and run a `specialized ocr` directly. In many ways, this method is ideally suited to service someone who doesn't want to continually pay a monthly or per scan amount or be limited in any way as far as throttling, rate limits, monthly payments, etc.... Training the ai is possible with this approach, but should be done carefully, and with clear, deterministic benchmarks in mind. Building, setting up and evaluating initially has a higher upfront cost and will also generally take longer to implement. Depending on the amount of use however, these costs can be significantly recouped in both monetary and functional value, increasingly so, over time.

The second approach is to utilize a 3rd party. In my research (I will update this `readme.md` when I publish the O`CR analysis report`), `Google Cloud Vision` has the greatest amount of flexibility, ease of use and is not cost prohibitive since you pay per scan. There's also hundreds of options to integrate with other AI plug ins and pre-built pipelines for hosting and scalable distribution. If hosting with Google Cloud, this solution can meet most businesses expectations in terms of quality and price.

## Future Implementation

For a production-ready microservice, several considerations and improvements will be necessary.

Right now, these are just two very rudimentary demos.

Plans to level up the ai in these two basic concepts is in the works.