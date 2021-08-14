### Motivation

I've been checking my budget and expenses using [ledger-dashboard](https://github.com/Ikke/ledger-dashboard) and org-mode babel. But they're not all in one place and some part of the check is a bit manual. My goal is to be able to both generate report and check the validity of my balances using a single command.


### Usage

##### `main.py`

- Is an example of how to use the ledger wrapper.
- Usage: `python main.py <file1> <file2>`

##### `report.py`

- Is an example of how to use the wrapper to produce a report.
- Usage: `python report.py <folder>`
- The folder structure is:
    ```
    - <folder>
      - <year>
        - <year><month>.ledger
    ```
