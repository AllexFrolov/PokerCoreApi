cmake_minimum_required(VERSION 3.22.1)

project(Montecarlo)

############################################################
# Create a library
############################################################

add_library(${PROJECT_NAME} SHARED src/evaluator.c montecarlo.c)
# add_library(utils::lib1 ALIAS ${PROJECT_NAME})

target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
)