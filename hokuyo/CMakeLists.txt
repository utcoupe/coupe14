#Configuration du projet
cmake_minimum_required(VERSION 2.8)
project(hokuyo_client)

FIND_PACKAGE(SDL REQUIRED)
SET(CMAKE_C_FLAGS "-std=c99")

set(EXECUTABLE_OUTPUT_PATH bin/)
set(EXEC_NAME hokuyo_client)

#Configurationdel'exécutable

file(
	GLOB_RECURSE
	source_files
	src/*
)

add_executable(
	${EXEC_NAME}
	${source_files}
)


INCLUDE_DIRECTORIES( ${SDL_INCLUDE_DIR} )
include_directories( /usr/local/include/urg_c )
target_link_libraries( hokuyo_client
	urg_c 
	SDL 
	m )
