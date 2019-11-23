add_library(underflow MODULE src/underflow.cpp)

include_directories(include)

target_compile_features(underflow PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(underflow PROPERTIES
        COMPILE_FLAGS "-g"
        )

if(APPLE)
    set_target_properties(underflow PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
            )
endif(APPLE)
