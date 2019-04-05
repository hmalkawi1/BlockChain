import zmq
from sawtooth_sdk.messaging.stream import Stream
from sawtooth_sdk.protobuf import events_pb2
from sawtooth_sdk.protobuf import client_event_pb2
from sawtooth_sdk.protobuf.validator_pb2 import Message


subscription = EventSubscription(
    event_type="notary/add",
    filters=[
        # Filter to only addresses in the "notary" namespace using a regex
        EventFilter(
            key="address",
            match_string="58504B.*",
            filter_type=EventFilter.REGEX_ANY)
    ])

############# SUBMIT THE SUBSCRIPTION REQUEST ###########
# Setup a connection to the validator
context = zmq.Context.instance()
service = context.socket(zmq.DEALER)
socket.connect("tcp://localhost:5556")

# Construct the request
request = ClientEventsSubscribeRequest(
    subscriptions=[subscription]).SerializeToString()

# Construct the message wrapper
correlation_id = "123" # This must be unique for all in-process requests
msg = Message(
    correlation_id=correlation_id,
    message_type=CLIENT_EVENTS_SUBSCRIBE_REQUEST,
    content=request)

# Send the request
socket.send_multipart([msg.SerializeToString()])


##################################################

############# RECIEVING RESPONSE #################################
# Receive the response
resp = socket.recv_multipart()[-1]

# Parse the message wrapper
msg = Message()
msg.ParseFromString(resp)

# Validate the response type
if msg.message_type != CLIENT_EVENTS_SUBSCRIBE_RESPONSE:
    print("Unexpected message type")
    return

# Parse the response
response = ClientEventsSubscribeResponse()
response.ParseFromString(msg.content)

# Validate the response status
if response.status != ClientEventsSubscribeResponse.OK:
  print("Subscription failed: {}".format(response.response_message))
  return


##################################################################



##################### LISTENING FOR EVENTS ###############################
while True:
  resp = socket.recv_multipart()[-1]

  # Parse the message wrapper
  msg = Message()
  msg.ParseFromString(resp)

  # Validate the response type
  if msg.message_type != CLIENT_EVENTS:
      print("Unexpected message type")
      return

  # Parse the response
  events = EventList()
  events.ParseFromString(msg.content)

  for event in events:
    print(event)

################################################################################