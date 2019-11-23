add_library(fpnan MODULE src/fpnan.cpp)

include_directories(include)

target_compile_features(fpnan PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(fpnan PROPERTIES
        COMPILE_FLAGS "-g"
        )

if(APPLE)
    set_target_properties(fpnan PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
            )
endif(APPLE)
