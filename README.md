# Patent PAIR Project

Disambiguating inventors based on the signature available in USPTO PAIR data.

### Data

An archive of PAIR data for inventors whose names resemble "Eric Anderson" can
be found at
[http://fungpatdownloads.s3.amazonaws.com/ericanderson_pair.7z](http://fungpatdownloads.s3.amazonaws.com/ericanderson_pair.7z)

### Prior Work

Previous work in the area of examining the signatures of individuals on
documents has concentrated around the verification of signatures as belonging
to a particular individual in the face of various levels of forgery. The
problem we are trying to solve is resolving which signatures resolve to a
particular individual, ignoring the possibility of forgery.

This simplifies our task in that we no longer have to consider the possibility
that certain features of our signature may be false identifiers. However, this
now complicates our situation in that we do not have an acknowledged
groundtruth for what signature maps to an individual.
