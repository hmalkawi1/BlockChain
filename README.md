# Hyperledger Sawtooth Notary
Application for distrbuted systems class to create a simple notary to record house sales on the blockchain with hyperledger sawtooth.


Run with `docker-compose up --build` in root directory. It should start the validator.

Attach to the client with  `docker exec -it notary-client bash` in a seperate terminal.  


There is only a single command to add a sale to the blockchain.

`./notary-client "First name" "Last name" "House ID"`

Useful docs reference [here](https://sawtooth.hyperledger.org/docs/core/releases/1.0.1/introduction.html)

And useful example ref by a sawtooth dev [here](github.com/inteldan/sawtooth-cookiejar)
