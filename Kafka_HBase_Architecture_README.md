
# Kafka Mechanism

### **Table: user_frametype_operations**

userid, frametype('sgl' | 'dbl'), operationid

### Topic: sgl_frames

userid, masked_timestamp, frameData

### Topic: dbl_frames

userid, masked_timestamp, frameData

### Topic: rekeyed_frames (merges sgl_frames, dbl_frames, and **user_frametype_operations**)

userid+'sgl'+operationid('raw')+timeid+masked_timestamp, frameData

userid+'dbl'+operationid('raw')+timeid+masked_timestamp, frameData

#### Consumers:

1. HBase Sink Connector sends the data to HBase
2. Compute Nodes read from 'rekeyed_frames' stream and process it according to operationId. They store result in processed_frames

### Topic: processed_frames

userid+'sgl'+operationid+timeid+masked_timestamp, frameData

#### Consumers:

1. HBase Sink Connector sends the data to HBase

### Topic: stored_frames

userid+'sgl'+operationid+timeid+masked_timestamp

#### Consumers:

1. Aggregator nodes read from stored_frames, read the data from HBase, figure out the parent timeid and masked_timestamp, recalculate the Parent, and store result in processed_frames
