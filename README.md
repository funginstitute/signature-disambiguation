# Patent PAIR Project

We're taking a look at the Patent PAIR data available through Google here:
[http://www.google.com/googlebooks/uspto-patents-pair.html](http://www.google.com/googlebooks/uspto-patents-pair.html)

PAIR stands for Patent Application Information Retrieval. From Google, the PAIR
data is available as zip files from URLs that looking like this:
`http://storage.googleapis.com/uspto-pair/applications/APP_NUM.zip`. Inside
each zip file, we want to look for `image-file-wrapper`, which contains PDF
documents of communication between the applicant and the patent examiner.

We have two goals for these PDF documents:

## 102/103 Extraction

When applying for a patent, the applicant makes certain "claims" in their
document. These claims can be rejected by the patent examiner on the basis that
someone else made these claims earlier. This will look something like the
following:

```
Claims 1, 3, 5, 12-13 are rejected under 35 U.S.C. 102(b) as being anticipated by Takagi (US 20040250593).       
```

For each of these PDFs, we want to get the patents that *block* other patents
(in this case, US20040250593).

### Packages Required

* ghostscript
* parallel
* tesseract

## Disambiguation through Signatures

We want to be able to disambiguate inventors by identifying their signatures in
the file. Need to look at computer vision techniques to pull out the
signatures, then link those signatures to patent and application numbers as
well as the name of the inventor on the document.


## Database

What kind of database do we need to store these records? How much disk space?
