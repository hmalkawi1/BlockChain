# Notes to self

Things I changed: 
 * `docker-compose.yaml`
        * did a control-f for all the `cookiejar` and replaced it with `notary` 
 * `pyprocessor`
    * `Dockerfile`
        * Replaced cookiejar with notary
    * `cookiejar_tp.py` -> `notary_tp.py`
        * changed shit in notary_tp.py
* `pyclient`
  * `cookiejar_tp.py` -> `notary_client.py`
  * Still working on functions for notary client
    NOTE: I'm splitting on '{' 

    changed url field in setup
    deleted other yaml docker-compose files