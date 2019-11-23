add_library(boundvalue MODULE src/boundvalue.cpp)

include_directories(include)

target_compile_features(boundvalue PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(boundvalue PROPERTIES
        COMPILE_FLAGS "-g"
        )

if(APPLE)
    set_target_properties(boundvalue PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
            )
endif(APPLE)
