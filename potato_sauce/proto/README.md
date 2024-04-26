This directory is for Protobuf definitions.

Protobuf is a data storage/exchange API by Google. You can find its public documentation. Some good things to know, to start off, are:

* Protobuf definitions (.proto files) can be transpiled into other languages.
  The *_pb2 libraries are auto-generated and need to be regenerated every time
  you change a .proto file.
* Install protoc and run build_proto.sh (with CWD set to the root of the repo)
  to regenerate the protos after making changes.
* Changes to proto definitions need to be carefully checked for backward
  compatibility issues, especially after the game has launched. Otherwise you'll
  brick everybody's save files.
