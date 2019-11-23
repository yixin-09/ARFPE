add_library(overflow MODULE src/overflow.cpp)

include_directories(include)

target_compile_features(overflow PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(overflow PROPERTIES
        COMPILE_FLAGS "-g"
        )

if(APPLE)
    set_target_properties(overflow PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
            )
endif(APPLE)
