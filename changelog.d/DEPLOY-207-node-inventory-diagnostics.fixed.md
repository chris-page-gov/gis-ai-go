- Identify the exact closed Node database inventory failure and report validated
  file sizes only when the expanded bound is exceeded. Accommodate the measured
  upstream database growth with a finite 4 GiB post-import size bound, retaining the
  256 MiB compressed bound, two-file contract and vulnerability policy. Reject empty
  files and unexpected directory or special entries before hashing.
