# Search all proto files
find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

file(GLOB PROTOBUF_FILELIST "*.proto")

find_program(_PROTOC protoc)
if(gRPC_FOUND)
  if(NOT TARGET gRPC::grpc++)
    find_package(gRPC CONFIG REQUIRED)
  endif()
  message(STATUS "Using gRPC ${gRPC_VERSION}")
  find_program(_GRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)
endif()

message(STATUS "Attempting to generate the protos:")
message(STATUS "_PROTOC=${_PROTOC}")
foreach(PROTOBUF_FILE ${PROTOBUF_FILELIST})
  message(STATUS "Generating: ${PROTOBUF_FILE}")
  if(gRPC_FOUND)
    message(STATUS "_GRPC_CPP_PLUGIN_EXECUTABLE=${_GRPC_CPP_PLUGIN_EXECUTABLE}")
    message(STATUS "Running in WD=${CMAKE_CURRENT_SOURCE_DIR}: ${_PROTOC} --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --grpc_out=. --plugin=protoc-gen-grpc=${_GRPC_CPP_PLUGIN_EXECUTABLE} --cpp_out=. ${PROTOBUF_FILE}")
    execute_process(COMMAND "${_PROTOC}" "--proto_path=${CMAKE_CURRENT_SOURCE_DIR}" "--grpc_out=." "--plugin=protoc-gen-grpc=${_GRPC_CPP_PLUGIN_EXECUTABLE}" "--cpp_out=." "${PROTOBUF_FILE}" WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} RESULT_VARIABLE gen_PROTO_RESULT)
  else()
    message(STATUS "gRPC not found, generating protobuf-only sources")
    message(STATUS "Running in WD=${CMAKE_CURRENT_SOURCE_DIR}: ${_PROTOC} --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --cpp_out=. ${PROTOBUF_FILE}")
    execute_process(COMMAND "${_PROTOC}" "--proto_path=${CMAKE_CURRENT_SOURCE_DIR}" "--cpp_out=." "${PROTOBUF_FILE}" WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} RESULT_VARIABLE gen_PROTO_RESULT)
  endif()
  message(STATUS "Result code ${gen_PROTO_RESULT}")
endforeach()

# Search all header and source files
file(GLOB hdrs "*.hpp" "*.pb.h")
file(GLOB srcs "*.cpp" "*.pb.cc")
message(STATUS ${hdrs})
dart_add_core_headers(${hdrs})
dart_add_core_sources(${srcs})

# Generate header for this namespace
dart_get_filename_components(header_names "proto headers" ${hdrs})
dart_generate_include_header_file(
  "${CMAKE_CURRENT_BINARY_DIR}/proto.hpp"
  "dart/proto/"
  ${header_names}
)

# Install
install(
  FILES ${hdrs} ${CMAKE_CURRENT_BINARY_DIR}/proto.hpp
  DESTINATION include/dart/proto
  COMPONENT headers
)
