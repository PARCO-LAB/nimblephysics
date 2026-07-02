if(NOT DARTPY_PYTHON_VERSION)
  set(DARTPY_PYTHON_VERSION 3.8 CACHE STRING "Choose the target Python version (e.g., 3.8, 3.9)" FORCE)
endif()

find_package(Python3 ${DARTPY_PYTHON_VERSION} COMPONENTS Interpreter Development REQUIRED)

# Find pybind11
# Needs to set PYBIND11_PYTHON_VERSION before finding pybind11
set(PYBIND11_PYTHON_VERSION ${DARTPY_PYTHON_VERSION})
find_package(pybind11 2.2.0 QUIET)
if(NOT pybind11_FOUND)
  message(STATUS "DART_BUILD_DARTPY is ON, but failed to find pybind11 >= "
    "2.2.0. Disabling _nimblephysics."
  )
  return()
endif()

message(STATUS "PYTHON_INCLUDE_DIRS: ${PYTHON_INCLUDE_DIRS}")
message(STATUS "pybind11_INCLUDE_DIRS: ${pybind11_INCLUDE_DIRS}")

file(GLOB_RECURSE _nimblephysics_headers "*.h" "*.hpp")
file(GLOB_RECURSE _nimblephysics_sources "*.cpp")

if(NOT gRPC_FOUND)
  set(_nimblephysics_sources_filtered)
  foreach(source ${_nimblephysics_sources})
    if(NOT source MATCHES "/(realtime|server)/")
      list(APPEND _nimblephysics_sources_filtered "${source}")
    endif()
  endforeach()
  set(_nimblephysics_sources ${_nimblephysics_sources_filtered})
endif()

# Build a Python extension module:
# pybind11_add_module(<name> [MODULE | SHARED] [EXCLUDE_FROM_ALL]
#                     [NO_EXTRAS] [SYSTEM] [THIN_LTO] source1 [source2 ...])
#
pybind11_add_module(_nimblephysics
  MODULE
  ${_nimblephysics_headers}
  ${_nimblephysics_sources}
)

# Add C++14 support
set_property(TARGET _nimblephysics PROPERTY CXX_STANDARD 14)
target_compile_options(_nimblephysics PRIVATE -fpermissive)
target_link_options(_nimblephysics PRIVATE
  "-Wl,-rpath,/tmp/nimblephysics-deps/usr/lib/x86_64-linux-gnu"
  "-Wl,-rpath,/tmp/nimblephysics-deps/draco-root/usr/lib/x86_64-linux-gnu"
)

target_include_directories(_nimblephysics
  SYSTEM PUBLIC
    ${Python3_INCLUDE_DIRS}
    ${pybind11_INCLUDE_DIRS}
  PRIVATE
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(_nimblephysics
  PUBLIC
    dart
    IPOPT::ipopt
    # dart-utils
    dart-utils-urdf
)

set_target_properties(_nimblephysics
  PROPERTIES
    PREFIX ""
    SUFFIX ".so"  # python uses '.so' extension even on macOS
    DEBUG_POSTFIX ""
)

# install(TARGETS _nimblephysics
#   LIBRARY DESTINATION "${PYTHON_SITE_PACKAGES}"
# )

list(REMOVE_ITEM _nimblephysics_headers
  ${CMAKE_CURRENT_LIST_DIR}/eigen_geometry_pybind.h
  ${CMAKE_CURRENT_LIST_DIR}/eigen_pybind.h
)
list(REMOVE_ITEM _nimblephysics_sources
  ${CMAKE_CURRENT_LIST_DIR}/eigen_geometry_pybind.cpp
)
dart_format_add(${_nimblephysics_headers} ${_nimblephysics_sources})
