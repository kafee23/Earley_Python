# Eearley Python

## Requirement

### Python version: 3.11

The main script uses no external libraries except for the `render_graph.py` used for render Graph after the main script
completed

## Directory Structure

- `main.py` entry point for program
- `lib_helper.py` implement Parser class
- `run_test_sample.py` the pre-defined test cases, it will output to `./out/sp1` ... `./out/sp4`
- `sppf.py` implement SPPF and SPPFNode and some enum class
- `render_graph.py` a small script for displaying images

## How to run

- In the `main.py`, change the input just like the Rust script
- Run the script
- Note: the output will be put at `./out/` instead of `./` as the Rust script

## Test procedure

- Run test case on Python and Rust versions
- Use `WinMerge` for checking similarity of all files (line by line) between 2 directories

