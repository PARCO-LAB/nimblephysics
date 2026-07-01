# Search all header and source files
file(GLOB hdrs "*.hpp")
file(GLOB srcs "*.cpp")
if(NOT gRPC_FOUND)
  list(REMOVE_ITEM srcs
    "${CMAKE_CURRENT_SOURCE_DIR}/MPCLocal.cpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/MPCRemote.cpp"
  )
endif()
dart_add_core_headers(${hdrs})
dart_add_core_sources(${srcs})

# Generate header for this namespace
dart_get_filename_components(header_names "realtime headers" ${hdrs})
dart_generate_include_header_file(
  "${CMAKE_CURRENT_BINARY_DIR}/realtime.hpp"
  "dart/realtime/"
  ${header_names}
)

# Install
install(
  FILES ${hdrs} ${CMAKE_CURRENT_BINARY_DIR}/realtime.hpp
  DESTINATION include/dart/realtime
  COMPONENT headers
)
