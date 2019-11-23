add_library(dividezero MODULE src/dividezero.cpp)

include_directories(include)

target_compile_features(dividezero PRIVATE cxx_range_for cxx_auto_type)

set_target_properties(dividezero PROPERTIES
        COMPILE_FLAGS "-g"
        )

if(APPLE)
    set_target_properties(dividezero PROPERTIES
            LINK_FLAGS "-undefined dynamic_lookup"
            )
endif(APPLE)
